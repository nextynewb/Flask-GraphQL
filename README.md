# Flask GraphQL with MongoDB Demo

A simple Flask application demonstrating GraphQL with MongoDB integration. Perfect for learning GraphQL basics!

## What You'll Learn

- Basic GraphQL concepts (Queries, Mutations, Types)
- How to integrate GraphQL with Flask
- Working with MongoDB in GraphQL resolvers
- Creating relationships between data types
- Using GraphiQL for testing queries

## Prerequisites

- Python 3.7+
- MongoDB running locally on port 27017
- Basic knowledge of Python and Flask

## Setup Instructions

### Quick Start (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   Make sure MongoDB is running on your local machine (default port 27017)

3. **Run the startup script:**
   ```bash
   python start.py
   ```
   This will check MongoDB, offer to seed the database, and start the Flask app!

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   Make sure MongoDB is running on your local machine (default port 27017)

3. **Seed the database:**
   ```bash
   python seeders.py
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Homepage: http://localhost:5000
   - GraphiQL Interface: http://localhost:5000/graphql

## Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "age": "number",
  "city": "string",
  "created_at": "datetime"
}
```

### Posts Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string",
  "author_id": "ObjectId",
  "tags": ["string"],
  "created_at": "datetime"
}
```

## GraphQL Schema

### Types

- **User**: Represents a user with posts relationship
- **Post**: Represents a blog post with author relationship

### Available Queries

1. **Get all users:**
   ```graphql
   {
     users {
       id
       name
       email
       age
       city
       posts {
         title
         tags
       }
     }
   }
   ```

2. **Get all posts with authors:**
   ```graphql
   {
     posts {
       id
       title
       content
       tags
       author {
         name
         email
         city
       }
     }
   }
   ```

3. **Get a specific user:**
   ```graphql
   {
     user(id: "USER_ID_HERE") {
       name
       email
       posts {
         title
         content
       }
     }
   }
   ```

4. **Search users by city:**
   ```graphql
   {
     usersByCity(city: "New York") {
       name
       email
       age
     }
   }
   ```

5. **Search posts by tag:**
   ```graphql
   {
     postsByTag(tag: "graphql") {
       title
       content
       author {
         name
       }
     }
   }
   ```

6. **Search posts by title:**
   ```graphql
   {
     postsByTitle(title: "GraphQL") {
       title
       content
       tags
     }
   }
   ```

### Available Mutations

1. **Create a new user:**
   ```graphql
   mutation {
     createUser(name: "John Smith", email: "john@example.com", age: 28, city: "Boston") {
       user {
         id
         name
         email
       }
     }
   }
   ```

2. **Create a new post:**
   ```graphql
   mutation {
     createPost(
       title: "My First Post"
       content: "This is the content of my first post!"
       authorId: "USER_ID_HERE"
       tags: ["tutorial", "graphql"]
     ) {
       post {
         id
         title
         author {
           name
         }
       }
     }
   }
   ```

## Key GraphQL Concepts Demonstrated

### 1. **Types and Fields**
- `User` and `Post` types with various field types (String, Int, List, etc.)
- Custom scalars for ObjectId and DateTime

### 2. **Relationships**
- One-to-many relationship: User has many Posts
- Many-to-one relationship: Post belongs to User

### 3. **Queries**
- Simple field selection
- Nested queries (getting author info with posts)
- Parameterized queries (search functions)
- Pagination support (limit/skip)

### 4. **Mutations**
- Creating new records
- Returning created data

### 5. **Resolvers**
- Custom logic for fetching related data
- Database integration with MongoDB

## Project Structure

```
flask-graphql/
├── app.py              # Main Flask application with GraphQL setup
├── seeders.py          # MongoDB data seeders
├── start.py            # Startup script (recommended way to run)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Tips for Learning GraphQL

1. **Start with simple queries** - Begin with basic field selection
2. **Use GraphiQL** - The interactive interface is perfect for experimentation
3. **Understand relationships** - Learn how to fetch related data efficiently
4. **Experiment with mutations** - Practice creating and modifying data
5. **Study the schema** - Use the GraphiQL docs panel to explore available operations

## Next Steps

Once you're comfortable with the basics, try:

- Adding more complex relationships
- Implementing authentication
- Adding real-time subscriptions
- Optimizing database queries
- Adding validation and error handling

## Troubleshooting

**MongoDB Connection Issues:**
- Ensure MongoDB is running: `brew services start mongodb/brew/mongodb-community` (macOS)
- Check connection string in both `app.py` and `seeders.py`

**GraphQL Errors:**
- Check the GraphiQL interface for detailed error messages
- Verify your query syntax against the schema documentation

Happy learning! 🚀 