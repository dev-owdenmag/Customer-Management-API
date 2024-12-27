from flask import Flask, requests, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = '897b3fa8a51b166038997f6e236b78977a3d63f1925d8dfe100754ed2e8e68bd'

jwt = JWTManager(app)

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
        token = create_access_token(identity=user.id)
        return jsonify({'token: token'}), 200
    return jsonify({'token': 'Invalid credentials'}), 401

@qpp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'balance': c.balance} for c in customers])

@app.route('/customers<int:id>', methods=['GET'])
@jwt_required
def get_customer(id):
    customer =Customer.query.get_or_404(id)
    return jsonify({'id': customer.id, 'name': customer.name, 'balance': customer.balance})

@app.route('/customers/<int:id>topup', methods=['POST'])
def topup_customer(id):
    customer = Customer.query.get_or_404(id)
    amount = request.json.get('amount', 0)
    if amount <= 0:
        return jsonify ({'message': 'Amount must be positive'}), 400
    customer.balance += amount
    db.session.commit()
    return jsonify({'message': 'Balance updated successfully', 'new_balance': customer.balance})

