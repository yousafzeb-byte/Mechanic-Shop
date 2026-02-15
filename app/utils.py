from jose import jwt, JWTError
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import bcrypt

# Secret key for JWT encoding/decoding
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def encode_token(customer_id):
    """
    Create a JWT token for a customer
    
    Args:
        customer_id: The ID of the customer
        
    Returns:
        A JWT token string
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),  # Token expires in 1 day
        'iat': datetime.utcnow(),  # Token issued at
        'sub': customer_id  # Subject (customer ID)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    """
    Decode a JWT token
    
    Args:
        token: The JWT token string
        
    Returns:
        The customer_id from the token, or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except JWTError:
        return None

def token_required(f):
    """
    Decorator to require a valid JWT token for a route
    
    The decorated function will receive the customer_id as an argument
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Decode the token
        customer_id = decode_token(token)
        
        if customer_id is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Pass the customer_id to the decorated function
        return f(customer_id, *args, **kwargs)
    
    return decorated_function
