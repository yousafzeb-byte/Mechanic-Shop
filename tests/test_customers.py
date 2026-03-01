import unittest
import json
from app import create_app, db
from app.models import Customer, ServiceTicket
from datetime import date


class TestCustomerBlueprint(unittest.TestCase):
    """Test cases for Customer blueprint endpoints"""

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
            # Create test customer
            from app.utils import hash_password
            self.test_customer = Customer(
                name="Test Customer",
                email="test@example.com",
                phone="555-1234",
                address="123 Test St",
                password=hash_password("password123")
            )
            db.session.add(self.test_customer)
            db.session.commit()
            self.customer_id = self.test_customer.id

    def tearDown(self):
        """Clean up after each test"""
        with self.app.app_context():
            # Clear many-to-many relationships first
            from app.models import service_mechanic, service_inventory
            db.session.execute(service_mechanic.delete())
            db.session.execute(service_inventory.delete())
            
            db.session.query(ServiceTicket).delete()
            db.session.query(Customer).delete()
            db.session.commit()

    # Positive Tests
    
    def test_create_customer_success(self):
        """Test successful customer creation"""
        response = self.client.post('/customers/', 
            json={
                "name": "New Customer",
                "email": "new@example.com",
                "phone": "555-5555",
                "address": "456 New St",
                "password": "newpass123"
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "New Customer")
        self.assertEqual(data['email'], "new@example.com")

    def test_get_all_customers_success(self):
        """Test retrieving all customers with pagination"""
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('customers', data)
        self.assertIn('pagination', data)
        self.assertTrue(len(data['customers']) > 0)

    def test_get_customer_by_id_success(self):
        """Test retrieving a specific customer"""
        response = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], "test@example.com")

    def test_login_success(self):
        """Test successful customer login"""
        response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('customer_id', data)
        self.assertEqual(data['message'], "Login successful")

    def test_get_my_tickets_with_token(self):
        """Test retrieving customer's tickets with valid token"""
        # First login to get token
        login_response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        token = json.loads(login_response.data)['token']

        # Then get tickets
        response = self.client.get('/customers/my-tickets',
            headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_customer_success(self):
        """Test successful customer update"""
        # Login to get token
        login_response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        token = json.loads(login_response.data)['token']

        # Update customer
        response = self.client.put(f'/customers/{self.customer_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                "name": "Updated Name",
                "phone": "555-9999"
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Updated Name")
        self.assertEqual(data['phone'], "555-9999")

    def test_delete_customer_success(self):
        """Test successful customer deletion"""
        # Login to get token
        login_response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        token = json.loads(login_response.data)['token']

        # Delete customer
        response = self.client.delete(f'/customers/{self.customer_id}',
            headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("deleted successfully", data['message'])

    def test_pagination_parameters(self):
        """Test pagination with custom parameters"""
        response = self.client.get('/customers/?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['per_page'], 5)

    # Negative Tests

    def test_create_customer_missing_required_field(self):
        """Test customer creation with missing required field"""
        response = self.client.post('/customers/',
            json={
                "name": "Incomplete Customer",
                "email": "incomplete@example.com"
                # Missing phone, address, password
            })
        self.assertEqual(response.status_code, 400)

    def test_create_customer_invalid_email(self):
        """Test customer creation with invalid email format"""
        response = self.client.post('/customers/',
            json={
                "name": "Test User",
                "email": "not-an-email",
                "phone": "555-1234",
                "address": "123 St",
                "password": "pass123"
            })
        # This should fail validation (exact status depends on schema validation)
        self.assertIn(response.status_code, [400, 422])

    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_login_nonexistent_user(self):
        """Test login with email that doesn't exist"""
        response = self.client.post('/customers/login',
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            })
        self.assertEqual(response.status_code, 401)

    def test_get_my_tickets_without_token(self):
        """Test accessing protected route without token"""
        response = self.client.get('/customers/my-tickets')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_get_my_tickets_invalid_token(self):
        """Test accessing protected route with invalid token"""
        response = self.client.get('/customers/my-tickets',
            headers={'Authorization': 'Bearer invalid_token_here'})
        self.assertEqual(response.status_code, 401)

    def test_get_customer_not_found(self):
        """Test retrieving non-existent customer"""
        response = self.client.get('/customers/99999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_update_customer_unauthorized(self):
        """Test updating another customer's account"""
        # Create second customer
        with self.app.app_context():
            from app.utils import hash_password
            customer2 = Customer(
                name="Customer 2",
                email="customer2@example.com",
                phone="555-2222",
                address="222 St",
                password=hash_password("pass123")
            )
            db.session.add(customer2)
            db.session.commit()
            customer2_id = customer2.id

        # Login as first customer
        login_response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        token = json.loads(login_response.data)['token']

        # Try to update second customer
        response = self.client.put(f'/customers/{customer2_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={"name": "Hacked Name"})
        self.assertEqual(response.status_code, 403)

    def test_delete_customer_unauthorized(self):
        """Test deleting another customer's account"""
        # Create second customer
        with self.app.app_context():
            from app.utils import hash_password
            customer2 = Customer(
                name="Customer 2",
                email="customer2@example.com",
                phone="555-2222",
                address="222 St",
                password=hash_password("pass123")
            )
            db.session.add(customer2)
            db.session.commit()
            customer2_id = customer2.id

        # Login as first customer
        login_response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        token = json.loads(login_response.data)['token']

        # Try to delete second customer
        response = self.client.delete(f'/customers/{customer2_id}',
            headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 403)

    def test_update_customer_not_found(self):
        """Test updating non-existent customer"""
        login_response = self.client.post('/customers/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            })
        token = json.loads(login_response.data)['token']

        response = self.client.put('/customers/99999',
            headers={'Authorization': f'Bearer {token}'},
            json={"name": "New Name"})
        # Will fail either due to authorization (403) or not found (404)
        self.assertIn(response.status_code, [403, 404])

    def test_rate_limiting(self):
        """Test rate limiting on customer creation"""
        # Make 6 requests (limit is 5 per minute)
        responses = []
        for i in range(6):
            response = self.client.post('/customers/',
                json={
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "phone": f"555-000{i}",
                    "address": f"{i} Street",
                    "password": "pass123"
                })
            responses.append(response)

        # 6th request should be rate limited
        self.assertEqual(responses[5].status_code, 429)


if __name__ == '__main__':
    unittest.main()
