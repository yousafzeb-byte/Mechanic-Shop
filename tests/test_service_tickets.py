import unittest
import json
from app import create_app, db
from app.models import ServiceTicket, Customer, Mechanic, Inventory
from datetime import date


class TestServiceTicketBlueprint(unittest.TestCase):
    """Test cases for Service Ticket blueprint endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up test application and database once for all tests"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:112233@localhost/mechanic_shop_test'
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up database after all tests"""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Set up test data before each test"""
        with self.app.app_context():
            from app.utils import hash_password
            
            # Create test customer
            self.test_customer = Customer(
                name="Test Customer",
                email="customer@test.com",
                phone="555-1234",
                address="123 Test St",
                password=hash_password("pass123")
            )
            db.session.add(self.test_customer)
            
            # Create test mechanic
            self.test_mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@test.com",
                phone="555-5678",
                address="456 Shop St",
                salary=60000.0
            )
            db.session.add(self.test_mechanic)
            
            # Create test inventory part
            self.test_part = Inventory(
                name="Test Part",
                price=25.99
            )
            db.session.add(self.test_part)
            
            db.session.commit()
            
            # Store IDs
            self.customer_id = self.test_customer.id
            self.mechanic_id = self.test_mechanic.id
            self.part_id = self.test_part.id
            
            # Create test service ticket
            self.test_ticket = ServiceTicket(
                VIN="1HGBH41JXMN109186",
                description="Oil change",
                service_date=date(2026, 2, 1),
                customer_id=self.customer_id
            )
            db.session.add(self.test_ticket)
            db.session.commit()
            self.ticket_id = self.test_ticket.id

    def tearDown(self):
        """Clean up after each test"""
        with self.app.app_context():
            # Clear many-to-many relationships first
            from app.models import service_mechanic, service_inventory
            db.session.execute(service_mechanic.delete())
            db.session.execute(service_inventory.delete())
            
            db.session.query(ServiceTicket).delete()
            db.session.query(Inventory).delete()
            db.session.query(Mechanic).delete()
            db.session.query(Customer).delete()
            db.session.commit()

    # Positive Tests

    def test_create_service_ticket_success(self):
        """Test successful service ticket creation"""
        response = self.client.post('/service-tickets/',
            json={
                "VIN": "2HGFC2F59KH542891",
                "description": "Brake replacement",
                "service_date": "2026-02-15",
                "customer_id": self.customer_id
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['VIN'], "2HGFC2F59KH542891")
        self.assertEqual(data['description'], "Brake replacement")

    def test_get_all_service_tickets_success(self):
        """Test retrieving all service tickets"""
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_get_service_ticket_by_id_success(self):
        """Test retrieving a specific service ticket"""
        response = self.client.get(f'/service-tickets/{self.ticket_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['VIN'], "1HGBH41JXMN109186")
        self.assertEqual(data['description'], "Oil change")

    def test_assign_mechanic_to_ticket_success(self):
        """Test assigning a mechanic to a service ticket"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("assigned", data['message'])

    def test_remove_mechanic_from_ticket_success(self):
        """Test removing a mechanic from a service ticket"""
        # First assign the mechanic
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        
        # Then remove
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("removed", data['message'])

    def test_edit_ticket_mechanics_bulk_success(self):
        """Test bulk editing mechanics on a ticket"""
        # Create another mechanic
        with self.app.app_context():
            mechanic2 = Mechanic(
                name="Mechanic Two",
                email="mechanic2@test.com",
                phone="555-7777",
                address="789 Shop St",
                salary=65000.0
            )
            db.session.add(mechanic2)
            db.session.commit()
            mechanic2_id = mechanic2.id

        # Assign first mechanic
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        
        # Use bulk edit to remove first and add second
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit',
            json={
                "remove_ids": [self.mechanic_id],
                "add_ids": [mechanic2_id]
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("updated successfully", data['message'])

    def test_add_part_to_ticket_success(self):
        """Test adding an inventory part to a service ticket"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("added", data['message'])

    def test_delete_service_ticket_success(self):
        """Test successful service ticket deletion"""
        response = self.client.delete(f'/service-tickets/{self.ticket_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("deleted successfully", data['message'])

    # Negative Tests

    def test_create_service_ticket_missing_field(self):
        """Test service ticket creation with missing required field"""
        response = self.client.post('/service-tickets/',
            json={
                "VIN": "1234567890",
                "description": "Incomplete ticket"
                # Missing service_date and customer_id
            })
        self.assertEqual(response.status_code, 400)

    def test_create_service_ticket_invalid_customer(self):
        """Test service ticket creation with non-existent customer"""
        response = self.client.post('/service-tickets/',
            json={
                "VIN": "1HGBH41JXMN109186",
                "description": "Test ticket",
                "service_date": "2026-02-01",
                "customer_id": 99999
            })
        # Should fail foreign key constraint
        self.assertIn(response.status_code, [400, 404, 500])

    def test_get_service_ticket_not_found(self):
        """Test retrieving non-existent service ticket"""
        response = self.client.get('/service-tickets/99999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_assign_nonexistent_mechanic(self):
        """Test assigning non-existent mechanic to ticket"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/99999')
        self.assertEqual(response.status_code, 404)

    def test_assign_mechanic_to_nonexistent_ticket(self):
        """Test assigning mechanic to non-existent ticket"""
        response = self.client.put(f'/service-tickets/99999/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 404)

    def test_assign_mechanic_already_assigned(self):
        """Test assigning mechanic that is already assigned"""
        # Assign mechanic
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        
        # Try to assign again
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("already assigned", data['message'])

    def test_remove_mechanic_not_assigned(self):
        """Test removing mechanic that is not assigned to ticket"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("not assigned", data['message'])

    def test_add_nonexistent_part(self):
        """Test adding non-existent part to ticket"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/99999')
        self.assertEqual(response.status_code, 404)

    def test_add_part_to_nonexistent_ticket(self):
        """Test adding part to non-existent ticket"""
        response = self.client.put(f'/service-tickets/99999/add-part/{self.part_id}')
        self.assertEqual(response.status_code, 404)

    def test_add_part_already_added(self):
        """Test adding part that is already added to ticket"""
        # Add part
        self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        
        # Try to add again
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("already added", data['message'])

    def test_delete_nonexistent_ticket(self):
        """Test deleting non-existent service ticket"""
        response = self.client.delete('/service-tickets/99999')
        self.assertEqual(response.status_code, 404)

    def test_edit_mechanics_invalid_json(self):
        """Test bulk edit with invalid JSON structure"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit',
            json={
                "invalid_field": [1, 2, 3]
            })
        # Should succeed but do nothing since remove_ids and add_ids default to []
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
