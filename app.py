from flask import Flask, send_from_directory, render_template
from flask_graphql import GraphQLView
import graphene
import pymongo
from bson import ObjectId
from datetime import datetime
from graphql import GraphQLError
from pymongo.errors import DuplicateKeyError
import bcrypt

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["graphql_demo"]

# Ensure unique index on email
try:
    db.users.create_index("email", unique=True)
except Exception:
    pass

# Password hashing utilities
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Custom scalar for ObjectId
class ObjectIdScalar(graphene.Scalar):
    """Custom scalar for MongoDB ObjectId"""
    
    @staticmethod
    def serialize(dt):
        return str(dt)
    
    @staticmethod
    def parse_literal(node):
        return ObjectId(node.value)
    
    @staticmethod
    def parse_value(value):
        return ObjectId(value)

# Custom scalar for DateTime
class DateTimeScalar(graphene.Scalar):
    """Custom scalar for DateTime"""
    
    @staticmethod
    def serialize(dt):
        return dt.isoformat()
    
    @staticmethod
    def parse_literal(node):
        return datetime.fromisoformat(node.value)
    
    @staticmethod
    def parse_value(value):
        return datetime.fromisoformat(value)

# GraphQL Types
class User(graphene.ObjectType):
    id = ObjectIdScalar()
    name = graphene.String()
    email = graphene.String()
    age = graphene.Int()
    city = graphene.String()
    created_at = DateTimeScalar()
    
    # Relationship: posts by this user
    posts = graphene.List(lambda: Post)
    
    def resolve_posts(self, info):
        posts = db.posts.find({"author_id": self.id})
        return [Post(id=post['_id'], **{k: v for k, v in post.items() if k != '_id'}) for post in posts]

class Post(graphene.ObjectType):
    id = ObjectIdScalar()
    title = graphene.String()
    content = graphene.String()
    author_id = ObjectIdScalar()
    tags = graphene.List(graphene.String)
    created_at = DateTimeScalar()
    
    # Relationship: author of this post
    author = graphene.Field(User)
    
    def resolve_author(self, info):
        user = db.users.find_one({"_id": self.author_id})
        return User(id=user['_id'], **{k: v for k, v in user.items() if k not in ['_id', 'password_hash']}) if user else None

# GraphQL Queries
class Query(graphene.ObjectType):
    # Single record queries
    user = graphene.Field(User, id=ObjectIdScalar(required=True))
    post = graphene.Field(Post, id=ObjectIdScalar(required=True))
    
    # List queries
    users = graphene.List(User, limit=graphene.Int(), skip=graphene.Int())
    posts = graphene.List(Post, limit=graphene.Int(), skip=graphene.Int())
    
    # Search queries
    users_by_city = graphene.List(User, city=graphene.String(required=True))
    posts_by_tag = graphene.List(Post, tag=graphene.String(required=True))
    posts_by_title = graphene.List(Post, title=graphene.String(required=True))
    
    def resolve_user(self, info, id):
        user = db.users.find_one({"_id": ObjectId(id)})
        return User(id=user['_id'], **{k: v for k, v in user.items() if k not in ['_id', 'password_hash']}) if user else None
    
    def resolve_post(self, info, id):
        post = db.posts.find_one({"_id": ObjectId(id)})
        return Post(id=post['_id'], **{k: v for k, v in post.items() if k != '_id'}) if post else None
    
    def resolve_users(self, info, limit=10, skip=0):
        users = db.users.find().skip(skip).limit(limit)
        return [User(id=user['_id'], **{k: v for k, v in user.items() if k not in ['_id', 'password_hash']}) for user in users]
    
    def resolve_posts(self, info, limit=10, skip=0):
        posts = db.posts.find().skip(skip).limit(limit)
        return [Post(id=post['_id'], **{k: v for k, v in post.items() if k != '_id'}) for post in posts]
    
    def resolve_users_by_city(self, info, city):
        users = db.users.find({"city": {"$regex": city, "$options": "i"}})
        return [User(id=user['_id'], **{k: v for k, v in user.items() if k not in ['_id', 'password_hash']}) for user in users]
    
    def resolve_posts_by_tag(self, info, tag):
        posts = db.posts.find({"tags": {"$in": [tag]}})
        return [Post(id=post['_id'], **{k: v for k, v in post.items() if k != '_id'}) for post in posts]
    
    def resolve_posts_by_title(self, info, title):
        posts = db.posts.find({"title": {"$regex": title, "$options": "i"}})
        return [Post(id=post['_id'], **{k: v for k, v in post.items() if k != '_id'}) for post in posts]

# GraphQL Mutations (for adding data)
class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        age = graphene.Int()
        city = graphene.String()
    
    user = graphene.Field(User)
    
    def mutate(self, info, name, email, password, age=None, city=None):
        if db.users.find_one({"email": email}):
            raise GraphQLError("Email already exists")
        
        # Hash the password before storing
        hashed_password = hash_password(password)

        user_data = {
            "name": name,
            "email": email,
            "password_hash": hashed_password,
            "age": age,
            "city": city,
            "created_at": datetime.now()
        }
        try:
            result = db.users.insert_one(user_data)
        except DuplicateKeyError:
            raise GraphQLError("Email already exists (duplicate)")
        user_data["_id"] = result.inserted_id
        # Don't include password_hash in the response for security
        return CreateUser(user=User(id=user_data['_id'], **{k: v for k, v in user_data.items() if k not in ['_id', 'password_hash']}))

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = ObjectIdScalar(required=True)
        tags = graphene.List(graphene.String)
    
    post = graphene.Field(Post)
    
    def mutate(self, info, title, content, author_id, tags=None):
        post_data = {
            "title": title,
            "content": content,
            "author_id": ObjectId(author_id),
            "tags": tags or [],
            "created_at": datetime.now()
        }
        result = db.posts.insert_one(post_data)
        post_data["_id"] = result.inserted_id
        return CreatePost(post=Post(id=post_data['_id'], **{k: v for k, v in post_data.items() if k != '_id'}))

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = ObjectIdScalar(required=True)

    ok = graphene.Boolean()
    deleted_count = graphene.Int()

    def mutate(self, info, id):
        if not db.users.find_one({"_id": ObjectId(id)}):
            raise GraphQLError("User not found")
        

        result = db.users.delete_one({"_id": ObjectId(id)})
        
        # After delete, delete all posts authored by this user
        db.posts.delete_many({"author_id": ObjectId(id)})
        return DeleteUser(ok=result.deleted_count > 0, deleted_count=result.deleted_count)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = ObjectIdScalar(required=True)

    ok = graphene.Boolean()
    deleted_count = graphene.Int()

    def mutate(self, info, id):
        result = db.posts.delete_one({"_id": ObjectId(id)})
        return DeletePost(ok=result.deleted_count > 0, deleted_count=result.deleted_count)

class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(User)

    def mutate(self, info, email, password):
        user = db.users.find_one({"email": email})
        if not user:
            return LoginUser(success=False, message="User not found", user=None)
        
        if verify_password(password, user['password_hash']):
            return LoginUser(
                success=True, 
                message="Login successful", 
                user=User(id=user['_id'], **{k: v for k, v in user.items() if k not in ['_id', 'password_hash']})
            )
        else:
            return LoginUser(success=False, message="Invalid password", user=None)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()
    delete_user = DeleteUser.Field()
    delete_post = DeletePost.Field()
    login_user = LoginUser.Field()

# Create GraphQL schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# Flask app setup
app = Flask(__name__)
app.debug = True

# Add GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)


@app.route('/create')
def create_page():
    return render_template('001_create.html')

@app.route('/delete')
def delete_page():
    return render_template('002_delete.html')

@app.route('/retrieve')
def retrieve_page():
    return render_template('003_retrieve.html')

@app.route('/login')
def login_page():
    return render_template('004_login.html')

@app.route('/auth')
def auth_page():
    return render_template('auth.html')

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask GraphQL Authentication Demo</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }
            .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
            .cta { background: white; color: #667eea; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin: 10px; border: 2px solid white; }
            .cta:hover { background: #667eea; color: white; }
            .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
            .feature { background: #f8f9fa; padding: 20px; border-radius: 10px; }
            .links { margin-top: 30px; }
            .links a { color: #667eea; text-decoration: none; margin: 0 15px; }
        </style>
    </head>
    <body>
                 <div class="hero">
             <h1>Flask GraphQL Authentication Demo</h1>
             <p>A complete authentication system with GraphQL, bcrypt encryption, and modern UI</p>
             <a href="/auth" class="cta">Start Here - Login/Register</a>
         </div>
         
         <div class="feature-grid">
             <div class="feature">
                 <h3>Secure Authentication</h3>
                 <p>Passwords encrypted with bcrypt, unique email validation, and secure GraphQL mutations</p>
             </div>
             <div class="feature">
                 <h3>Modern UI</h3>
                 <p>Clean, responsive interface with tabbed login/register forms and user dashboard</p>
             </div>
             <div class="feature">
                 <h3>GraphQL Powered</h3>
                 <p>All operations use GraphQL with proper error handling and data validation</p>
             </div>
         </div>
        
        <h2>Quick Test Accounts</h2>
        <ul>
            <li><strong>john@example.com</strong> / password123</li>
            <li><strong>jane@example.com</strong> / mypassword</li>
            <li><strong>bob@example.com</strong> / bobsecret</li>
        </ul>
        
        <div class="links">
            <h3>Developer Tools:</h3>
            <a href="/graphql">GraphiQL Interface</a>
            <a href="/retrieve">View All Data</a>
            <a href="/create">Simple Create Form</a>
            <a href="/login">Basic Login Test</a>
            <a href="/delete">Delete Tools</a>
        </div>
    </body>
    </html>
    '''
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005) 