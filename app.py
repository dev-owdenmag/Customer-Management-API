from flask import Flask, request, jsonify
from database import init_app, db
from flask_bcrypt import Bcrypt
from models import User, Customer
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

#Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize database
init_app(app)

bcrypt = Bcrypt(app)

# Ensure tables are created and data is seeded before the first request
@app.before_request
def setup_database():
    db.create_all()

    # Seed data if the database is empty
    if not User.query.first():
        # Create an admin user
        admin = User(username='admin', password=bcrypt.generate_password_hash('admin123').decode('utf-8'))
        
        # Create sample customers
        customers = [
            Customer(name='Customer 1', balance=100.0),
            Customer(name='Customer 2', balance=200.0)
        ]

        # Add and commit the data
        db.session.add(admin)
        db.session.add_all(customers)
        db.session.commit()
        print("Database seeded successfully!")

app.config['JWT_SECRET_KEY'] = '897b3fa8a51b166038997f6e236b78977a3d63f1925d8dfe100754ed2e8e68bd'

jwt = JWTManager(app)

# @app.before_first_request

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        response = {
            "token": token,
            "roles": list({"admin", "user"})
        }
        return jsonify(response), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'balance': c.balance} for c in customers])

@app.route('/customers<int:id>', methods=['GET'])
@jwt_required
def get_customer(id):
    customer =Customer.query.get_or_404(id)
    return jsonify({'id': customer.id, 'name': customer.name, 'balance': customer.balance})

@app.route('/customers/<int:id>/topup', methods=['POST'])
@jwt_required()
def topup_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    amount = data.get('amount', 0)

    if amount <= 0:
        return jsonify({"message": "Amount must be positive"}), 400

    customer.balance += amount
    db.session.commit()

    return jsonify({
        "message": "Balance updated successfully",
        "new_balance": customer.balance
    }), 200

if __name__=='__main__':
    app.run(debug=True)