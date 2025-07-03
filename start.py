#!/usr/bin/env python3
"""
Startup script for Flask GraphQL Demo
This script will seed the database and start the Flask application
"""

import subprocess
import sys
import time
import pymongo


def check_mongodb():
    """Check if MongoDB is running"""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running")
        return True
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ MongoDB is not running")
        print("Please start MongoDB first:")
        print("  - macOS: brew services start mongodb/brew/mongodb-community")
        print("  - Linux: sudo systemctl start mongod")
        print("  - Windows: net start MongoDB")
        return False

def seed_database():
    """Run the database seeders"""
    print("\n🌱 Seeding database...")
    try:
        subprocess.run([sys.executable, "seeders.py"], check=True)
        print("Database seeded successfully")
        return True
    except subprocess.CalledProcessError:
        print("Failed to seed database")
        return False

def start_flask_app():
    """Start the Flask application"""
    print("\nStarting Flask application...")
    print("Access the app at: http://localhost:5000")
    print("GraphiQL interface: http://localhost:5000/graphql")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except subprocess.CalledProcessError:
        print("Failed to start Flask application")

def main():
    print("Flask GraphQL Demo Startup Script")
    print("=====================================")
    
    # Check if MongoDB is running
    if not check_mongodb():
        sys.exit(1)
    
    # Ask user if they want to seed the database
    while True:
        choice = input("\n🌱 Do you want to seed the database? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            if not seed_database():
                sys.exit(1)
            break
        elif choice in ['n', 'no']:
            print("Skipping database seeding...")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")
    
    # Start the Flask application
    start_flask_app()

if __name__ == "__main__":
    main() 