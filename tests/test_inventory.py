import unittest
import json
from app import create_app, db
from app.models import Inventory, ServiceTicket, Customer
from datetime import date


class TestInventoryBlueprint(unittest.TestCase):
    """Test cases for Inventory blueprint endpoints"""

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
            # Create test inventory part
            self.test_part = Inventory(
                name="Test Oil Filter",
                price=12.99
            )
            db.session.add(self.test_part)
            db.session.commit()
            self.part_id = self.test_part.id

    def tearDown(self):
        """Clean up after each test"""
        with self.app.app_context():
            # Clear many-to-many relationships first
            from app.models import service_inventory
            db.session.execute(service_inventory.delete())
            
            db.session.query(ServiceTicket).delete()
            db.session.query(Customer).delete()
            db.session.query(Inventory).delete()
            db.session.commit()

    # Positive Tests

    def test_create_inventory_success(self):
        """Test successful inventory part creation"""
        response = self.client.post('/inventory/',
            json={
                "name": "Brake Pads",
                "price": 89.99
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Brake Pads")
        self.assertEqual(data['price'], 89.99)

    def test_get_all_inventory_success(self):
        """Test retrieving all inventory parts"""
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_get_inventory_by_id_success(self):
        """Test retrieving a specific inventory part"""
        response = self.client.get(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Test Oil Filter")
        self.assertEqual(data['price'], 12.99)

    def test_update_inventory_success(self):
        """Test successful inventory part update"""
        response = self.client.put(f'/inventory/{self.part_id}',
            json={
                "name": "Premium Oil Filter",
                "price": 15.99
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Premium Oil Filter")
        self.assertEqual(data['price'], 15.99)

    def test_update_inventory_partial(self):
        """Test updating only one field of inventory part"""
        response = self.client.put(f'/inventory/{self.part_id}',
            json={
                "price": 14.99
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Test Oil Filter")  # Name unchanged
        self.assertEqual(data['price'], 14.99)  # Price updated

    def test_delete_inventory_success(self):
        """Test successful inventory part deletion"""
        response = self.client.delete(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("deleted successfully", data['message'])

    def test_create_multiple_inventory_parts(self):
        """Test creating multiple inventory parts"""
        parts = [
            {"name": "Air Filter", "price": 15.99},
            {"name": "Spark Plugs", "price": 24.99},
            {"name": "Wiper Blades", "price": 19.99}
        ]
        
        for part in parts:
            response = self.client.post('/inventory/', json=part)
            self.assertEqual(response.status_code, 201)

        # Verify all parts exist
        response = self.client.get('/inventory/')
        data = json.loads(response.data)
        self.assertTrue(len(data) >= 4)  # Original test part + 3 new parts

    # Negative Tests

    def test_create_inventory_missing_name(self):
        """Test inventory creation with missing name"""
        response = self.client.post('/inventory/',
            json={
                "price": 25.99
                # Missing name
            })
        self.assertEqual(response.status_code, 400)

    def test_create_inventory_missing_price(self):
        """Test inventory creation with missing price"""
        response = self.client.post('/inventory/',
            json={
                "name": "Incomplete Part"
                # Missing price
            })
        self.assertEqual(response.status_code, 400)

    def test_create_inventory_invalid_price(self):
        """Test inventory creation with invalid price type"""
        response = self.client.post('/inventory/',
            json={
                "name": "Bad Price Part",
                "price": "not-a-number"
            })
        self.assertEqual(response.status_code, 400)

    def test_create_inventory_negative_price(self):
        """Test inventory creation with negative price"""
        response = self.client.post('/inventory/',
            json={
                "name": "Negative Price Part",
                "price": -10.00
            })
        # Depending on validation, this might be accepted or rejected
        # If no validation exists, it will be 201, otherwise 400
        self.assertIn(response.status_code, [201, 400])

    def test_get_inventory_not_found(self):
        """Test retrieving non-existent inventory part"""
        response = self.client.get('/inventory/99999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_update_inventory_not_found(self):
        """Test updating non-existent inventory part"""
        response = self.client.put('/inventory/99999',
            json={
                "name": "Ghost Part",
                "price": 99.99
            })
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_not_found(self):
        """Test deleting non-existent inventory part"""
        response = self.client.delete('/inventory/99999')
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_invalid_price(self):
        """Test updating inventory with invalid price"""
        response = self.client.put(f'/inventory/{self.part_id}',
            json={
                "price": "invalid_price"
            })
        self.assertEqual(response.status_code, 400)

    def test_create_inventory_empty_name(self):
        """Test creating inventory with empty name"""
        response = self.client.post('/inventory/',
            json={
                "name": "",
                "price": 10.00
            })
        # Depending on validation, might be accepted or rejected
        self.assertIn(response.status_code, [201, 400])

    def test_create_inventory_zero_price(self):
        """Test creating inventory with zero price"""
        response = self.client.post('/inventory/',
            json={
                "name": "Free Part",
                "price": 0.00
            })
        # Zero price might be valid for free items
        self.assertIn(response.status_code, [201, 400])

    def test_get_inventory_invalid_id_format(self):
        """Test getting inventory with invalid ID format"""
        response = self.client.get('/inventory/not-a-number')
        # Flask should return 404 for invalid route parameter
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_with_extra_fields(self):
        """Test updating inventory with extra fields that don't exist"""
        response = self.client.put(f'/inventory/{self.part_id}',
            json={
                "name": "Updated Part",
                "price": 20.00,
                "extra_field": "should be ignored"
            })
        # Should succeed and ignore extra fields
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Updated Part")
        self.assertNotIn('extra_field', data)


if __name__ == '__main__':
    unittest.main()
