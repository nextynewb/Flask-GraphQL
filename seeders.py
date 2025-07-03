import pymongo
from datetime import datetime
import random
import bcrypt

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["graphql_demo"]

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def clear_collections():
    """Clear existing data"""
    db.users.delete_many({})
    db.posts.delete_many({})
    print("Collections cleared!")

def seed_users():
    """Seed users collection"""
    users = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "password_hash": hash_password("password123"),
            "age": 28,
            "city": "New York",
            "created_at": datetime.now()
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password_hash": hash_password("mypassword"),
            "age": 25,
            "city": "Los Angeles",
            "created_at": datetime.now()
        },
        {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "password_hash": hash_password("bobsecret"),
            "age": 32,
            "city": "Chicago",
            "created_at": datetime.now()
        },
        {
            "name": "Alice Brown",
            "email": "alice@example.com",
            "password_hash": hash_password("alicepass"),
            "age": 29,
            "city": "Seattle",
            "created_at": datetime.now()
        },
        {
            "name": "Charlie Wilson",
            "email": "charlie@example.com",
            "password_hash": hash_password("charlie456"),
            "age": 35,
            "city": "San Francisco",
            "created_at": datetime.now()
        }
    ]
    
    result = db.users.insert_many(users)
    print(f"Inserted {len(result.inserted_ids)} users")
    return result.inserted_ids

def seed_posts(user_ids):
    """Seed posts collection"""
    posts = [
        {
            "title": "Introduction to GraphQL",
            "content": "GraphQL is a powerful query language for APIs that provides a complete and understandable description of the data in your API.",
            "author_id": random.choice(user_ids),
            "tags": ["graphql", "api", "web development"],
            "created_at": datetime.now()
        },
        {
            "title": "Getting Started with Flask",
            "content": "Flask is a lightweight WSGI web application framework in Python. It's designed to make getting started quick and easy.",
            "author_id": random.choice(user_ids),
            "tags": ["flask", "python", "web development"],
            "created_at": datetime.now()
        },
        {
            "title": "MongoDB Basics",
            "content": "MongoDB is a source-available cross-platform document-oriented database program. It uses JSON-like documents with optional schemas.",
            "author_id": random.choice(user_ids),
            "tags": ["mongodb", "database", "nosql"],
            "created_at": datetime.now()
        },
        {
            "title": "Building APIs with Python",
            "content": "Python offers several frameworks for building robust APIs. Flask and FastAPI are among the most popular choices.",
            "author_id": random.choice(user_ids),
            "tags": ["python", "api", "backend"],
            "created_at": datetime.now()
        },
        {
            "title": "Frontend Development Trends",
            "content": "Modern frontend development has evolved significantly with frameworks like React, Vue, and Angular leading the way.",
            "author_id": random.choice(user_ids),
            "tags": ["frontend", "javascript", "react"],
            "created_at": datetime.now()
        },
        {
            "title": "Database Design Principles",
            "content": "Good database design is crucial for application performance and maintainability. Here are some key principles to follow.",
            "author_id": random.choice(user_ids),
            "tags": ["database", "design", "architecture"],
            "created_at": datetime.now()
        }
    ]
    
    result = db.posts.insert_many(posts)
    print(f"Inserted {len(result.inserted_ids)} posts")
    return result.inserted_ids

def seed_database():
    """Main seeding function"""
    print("Starting database seeding...")
    
    # Clear existing data
    clear_collections()
    
    # Seed users first
    user_ids = seed_users()
    
    # Seed posts with user references
    post_ids = seed_posts(user_ids)
    
    print("Database seeding completed!")
    print(f"Created {len(user_ids)} users and {len(post_ids)} posts")

if __name__ == "__main__":
    seed_database()
