# Flask GraphQL with MongoDB Demo

A simple Flask application demonstrating GraphQL with MongoDB integration. Perfect for learning GraphQL basics!

## Contents

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

## JavaScript Integration Examples

This section provides ready-to-use code examples for accessing GraphQL data from your frontend using both jQuery AJAX and the Fetch API.

### Using jQuery AJAX

**Include jQuery in your HTML:**
```html
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

#### 1. **Query: Get All Users**
```javascript
const query = `{
  users {
    id
    name
    email
    city
    posts {
      title
      tags
    }
  }
}`;

$.ajax({
  url: '/graphql',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ query }),
  success: function(response) {
    console.log('Users:', response.data.users);
    // Process the data
    response.data.users.forEach(user => {
      console.log(`${user.name} from ${user.city}`);
    });
  },
  error: function(xhr, status, error) {
    console.error('Error:', error);
  }
});
```

#### 2. **Mutation: Create User**
```javascript
const mutation = `
  mutation CreateUser($name: String!, $email: String!, $password: String!, $age: Int, $city: String) {
    createUser(name: $name, email: $email, password: $password, age: $age, city: $city) {
      user {
        id
        name
        email
      }
    }
  }`;

const variables = {
  name: "John Doe",
  email: "john@example.com",
  password: "securepassword",
  age: 30,
  city: "New York"
};

$.ajax({
  url: '/graphql',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ query: mutation, variables }),
  success: function(response) {
    if (response.data?.createUser?.user) {
      console.log('User created:', response.data.createUser.user);
    } else if (response.errors) {
      console.error('GraphQL Error:', response.errors[0].message);
    }
  },
  error: function(xhr, status, error) {
    console.error('Request failed:', error);
  }
});
```

#### 3. **Mutation: Login User**
```javascript
const loginMutation = `
  mutation LoginUser($email: String!, $password: String!) {
    loginUser(email: $email, password: $password) {
      success
      message
      user {
        id
        name
        email
      }
    }
  }`;

const credentials = {
  email: "john@example.com",
  password: "securepassword"
};

$.ajax({
  url: '/graphql',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ query: loginMutation, variables: credentials }),
  success: function(response) {
    const result = response.data.loginUser;
    if (result.success) {
      console.log('Login successful:', result.user);
      // Store user data, redirect, etc.
    } else {
      console.log('Login failed:', result.message);
    }
  },
  error: function(xhr, status, error) {
    console.error('Login request failed:', error);
  }
});
```

#### 4. **Query with Variables: Search Posts**
```javascript
const searchQuery = `
  query SearchPosts($tag: String!) {
    postsByTag(tag: $tag) {
      id
      title
      content
      author {
        name
        email
      }
    }
  }`;

$.ajax({
  url: '/graphql',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ 
    query: searchQuery, 
    variables: { tag: "graphql" }
  }),
  success: function(response) {
    console.log('Posts found:', response.data.postsByTag);
  },
  error: function(xhr, status, error) {
    console.error('Search failed:', error);
  }
});
```

### Using Fetch API

#### 1. **Query: Get All Users**
```javascript
const query = `{
  users {
    id
    name
    email
    city
    posts {
      title
      tags
    }
  }
}`;

fetch('/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ query })
})
.then(response => response.json())
.then(data => {
  console.log('Users:', data.data.users);
  // Process the data
  data.data.users.forEach(user => {
    console.log(`${user.name} from ${user.city}`);
  });
})
.catch(error => {
  console.error('Error:', error);
});
```

#### 2. **Mutation: Create User**
```javascript
const mutation = `
  mutation CreateUser($name: String!, $email: String!, $password: String!, $age: Int, $city: String) {
    createUser(name: $name, email: $email, password: $password, age: $age, city: $city) {
      user {
        id
        name
        email
      }
    }
  }`;

const variables = {
  name: "Jane Smith",
  email: "jane@example.com",
  password: "mypassword",
  age: 25,
  city: "Los Angeles"
};

fetch('/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ query: mutation, variables })
})
.then(response => response.json())
.then(data => {
  if (data.data?.createUser?.user) {
    console.log('User created:', data.data.createUser.user);
  } else if (data.errors) {
    console.error('GraphQL Error:', data.errors[0].message);
  }
})
.catch(error => {
  console.error('Request failed:', error);
});
```

#### 3. **Async/Await Pattern**
```javascript
async function loginUser(email, password) {
  const mutation = `
    mutation LoginUser($email: String!, $password: String!) {
      loginUser(email: $email, password: $password) {
        success
        message
        user {
          id
          name
          email
        }
      }
    }`;

  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        query: mutation, 
        variables: { email, password }
      })
    });

    const data = await response.json();
    const result = data.data.loginUser;
    
    if (result.success) {
      console.log('Login successful:', result.user);
      return result.user;
    } else {
      throw new Error(result.message);
    }
  } catch (error) {
    console.error('Login failed:', error.message);
    throw error;
  }
}

// Usage
loginUser('john@example.com', 'password123')
  .then(user => {
    // Handle successful login
    console.log('Logged in user:', user);
  })
  .catch(error => {
    // Handle login error
    console.log('Login error:', error.message);
  });
```

#### 4. **Delete Operation**
```javascript
async function deleteUser(userId) {
  const mutation = `
    mutation DeleteUser($id: ObjectIdScalar!) {
      deleteUser(id: $id) {
        ok
        deletedCount
      }
    }`;

  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        query: mutation, 
        variables: { id: userId }
      })
    });

    const data = await response.json();
    
    if (data.data.deleteUser.ok) {
      console.log('User deleted successfully');
      return true;
    } else {
      throw new Error('Delete failed');
    }
  } catch (error) {
    console.error('Delete error:', error);
    return false;
  }
}
```

### Error Handling Best Practices

#### Comprehensive Error Handling with jQuery:
```javascript
$.ajax({
  url: '/graphql',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ query, variables }),
  success: function(response) {
    // Check for GraphQL errors
    if (response.errors) {
      console.error('GraphQL Errors:', response.errors);
      response.errors.forEach(error => {
        console.error('- ' + error.message);
      });
      return;
    }
    
    // Process successful response
    console.log('Success:', response.data);
  },
  error: function(xhr, status, error) {
    console.error('HTTP Error:', status, error);
    
    // Try to parse error response
    try {
      const errorData = JSON.parse(xhr.responseText);
      console.error('Server Error:', errorData);
    } catch (e) {
      console.error('Raw Error:', xhr.responseText);
    }
  }
});
```

#### Comprehensive Error Handling with Fetch:
```javascript
async function graphqlRequest(query, variables = {}) {
  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, variables })
    });

    // Check HTTP status
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Check for GraphQL errors
    if (data.errors) {
      throw new Error('GraphQL Error: ' + data.errors[0].message);
    }

    return data.data;
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}

// Usage
graphqlRequest(query, variables)
  .then(data => console.log('Success:', data))
  .catch(error => console.error('Error:', error.message));
```

### Quick Reference: Common Patterns

**Form Submission with jQuery:**
```javascript
$('#myForm').on('submit', function(e) {
  e.preventDefault();
  
  const formData = {
    name: $('#name').val(),
    email: $('#email').val(),
    // ... other fields
  };
  
  // Your GraphQL mutation here
});
```

**Loading States:**
```javascript
// Show loading
$('#submitBtn').prop('disabled', true).text('Loading...');

// Hide loading (in success/error callbacks)
$('#submitBtn').prop('disabled', false).text('Submit');
```

**Dynamic Content Updates:**
```javascript
// Update DOM with received data
response.data.users.forEach(user => {
  $('#usersList').append(`
    <div class="user">
      <h3>${user.name}</h3>
      <p>${user.email}</p>
    </div>
  `);
});
```

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

