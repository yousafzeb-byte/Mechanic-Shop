import unittest
import json
from app import create_app, db
from app.models import Mechanic, ServiceTicket, Customer
from datetime import date


class TestMechanicBlueprint(unittest.TestCase):
    """Test cases for Mechanic blueprint endpoints"""

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
            # Create test mechanic
            self.test_mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@test.com",
                phone="555-1111",
                address="100 Shop St",
                salary=50000.0
            )
            db.session.add(self.test_mechanic)
            db.session.commit()
            self.mechanic_id = self.test_mechanic.id

    def tearDown(self):
        """Clean up after each test"""
        with self.app.app_context():
            # Clear many-to-many relationships first
            from app.models import service_mechanic, service_inventory
            db.session.execute(service_mechanic.delete())
            db.session.execute(service_inventory.delete())
            
            db.session.query(ServiceTicket).delete()
            db.session.query(Mechanic).delete()
            db.session.query(Customer).delete()
            db.session.commit()

    # Positive Tests

    def test_create_mechanic_success(self):
        """Test successful mechanic creation"""
        response = self.client.post('/mechanics/',
            json={
                "name": "New Mechanic",
                "email": "new.mechanic@shop.com",
                "phone": "555-2222",
                "address": "200 Workshop Ave",
                "salary": 60000.0
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "New Mechanic")
        self.assertEqual(data['salary'], 60000.0)

    def test_get_all_mechanics_success(self):
        """Test retrieving all mechanics"""
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_get_mechanic_by_id_success(self):
        """Test retrieving a specific mechanic"""
        response = self.client.get(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], "mechanic@test.com")
        self.assertEqual(data['name'], "Test Mechanic")

    def test_get_mechanics_by_tickets(self):
        """Test retrieving mechanics sorted by ticket count"""
        # Create customer and service tickets
        with self.app.app_context():
            from app.utils import hash_password
            customer = Customer(
                name="Test Customer",
                email="customer@test.com",
                phone="555-3333",
                address="300 St",
                password=hash_password("pass123")
            )
            db.session.add(customer)
            db.session.commit()

            # Create tickets and assign to mechanic
            ticket1 = ServiceTicket(
                VIN="1HGBH41JXMN109186",
                description="Oil change",
                service_date=date(2026, 2, 1),
                customer_id=customer.id
            )
            ticket2 = ServiceTicket(
                VIN="2HGFC2F59KH542891",
                description="Brake repair",
                service_date=date(2026, 2, 5),
                customer_id=customer.id
            )
            db.session.add_all([ticket1, ticket2])
            db.session.commit()

            # Assign mechanic to tickets
            mechanic = db.session.get(Mechanic, self.mechanic_id)
            mechanic.service_tickets.append(ticket1)
            mechanic.service_tickets.append(ticket2)
            db.session.commit()

        # Test the endpoint
        response = self.client.get('/mechanics/by-tickets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        # Verify ticket_count field exists
        self.assertIn('ticket_count', data[0])

    def test_update_mechanic_success(self):
        """Test successful mechanic update"""
        response = self.client.put(f'/mechanics/{self.mechanic_id}',
            json={
                "name": "Updated Mechanic",
                "salary": 75000.0
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Updated Mechanic")
        self.assertEqual(data['salary'], 75000.0)

    def test_delete_mechanic_success(self):
        """Test successful mechanic deletion"""
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("deleted successfully", data['message'])

    # Negative Tests

    def test_create_mechanic_missing_required_field(self):
        """Test mechanic creation with missing required field"""
        response = self.client.post('/mechanics/',
            json={
                "name": "Incomplete Mechanic",
                "email": "incomplete@shop.com"
                # Missing phone, address, salary
            })
        self.assertEqual(response.status_code, 400)

    def test_create_mechanic_invalid_salary(self):
        """Test mechanic creation with invalid salary type"""
        response = self.client.post('/mechanics/',
            json={
                "name": "Bad Salary Mechanic",
                "email": "badsalary@shop.com",
                "phone": "555-4444",
                "address": "400 St",
                "salary": "not-a-number"
            })
        self.assertEqual(response.status_code, 400)

    def test_get_mechanic_not_found(self):
        """Test retrieving non-existent mechanic"""
        response = self.client.get('/mechanics/99999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_update_mechanic_not_found(self):
        """Test updating non-existent mechanic"""
        response = self.client.put('/mechanics/99999',
            json={"name": "Ghost Mechanic"})
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic_not_found(self):
        """Test deleting non-existent mechanic"""
        response = self.client.delete('/mechanics/99999')
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_invalid_data(self):
        """Test updating mechanic with invalid data"""
        response = self.client.put(f'/mechanics/{self.mechanic_id}',
            json={
                "salary": "invalid_salary_value"
            })
        # Should fail validation
        self.assertEqual(response.status_code, 400)

    def test_create_duplicate_email(self):
        """Test creating mechanic with duplicate email"""
        # Create first mechanic
        response1 = self.client.post('/mechanics/',
            json={
                "name": "Mechanic One",
                "email": "duplicate@shop.com",
                "phone": "555-5555",
                "address": "500 St",
                "salary": 55000.0
            })
        self.assertEqual(response1.status_code, 201)

        # Try to create second mechanic with same email
        response2 = self.client.post('/mechanics/',
            json={
                "name": "Mechanic Two",
                "email": "duplicate@shop.com",
                "phone": "555-6666",
                "address": "600 St",
                "salary": 57000.0
            })
        # Should fail due to unique constraint
        self.assertIn(response2.status_code, [400, 409, 500])


if __name__ == '__main__':
    unittest.main()
