from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    rented = db.Column(db.Boolean, default=False)
    rented_to = db.Column(db.Integer, db.ForeignKey('customer.id'))
    rented_distance = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    customers = Customer.query.all()
    cars = Car.query.all()
    rented_cars = Car.query.filter_by(rented=True).all()
    return render_template('index.html', customers=customers, cars=cars, rented_cars=rented_cars)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    email = request.form['email']
    new_customer = Customer(name=name, email=email)
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer_to_delete = Customer.query.get_or_404(id)
    db.session.delete(customer_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_car', methods=['POST'])
def add_car():
    brand = request.form['brand']
    model = request.form['model']
    rented = 'rented' in request.form
    customer_id = request.form.get('customer')
    distance = int(request.form.get('distance', 0))
    
    new_car = Car(brand=brand, model=model, rented=rented, rented_distance=distance)
    if rented and customer_id:
        new_car.rented_to = int(customer_id) # Konvertiere die Kunden-ID in eine Ganzzahl
    db.session.add(new_car)
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/edit_car/<int:id>', methods=['GET', 'POST'])
def edit_car(id):
    car = Car.query.get_or_404(id)
    if request.method == 'POST':
        car.brand = request.form['brand']
        car.model = request.form['model']
        car.rented = 'rented' in request.form
        car.rented_to = request.form['customer']
        car.rented_distance = request.form['distance']
        db.session.commit()
        return redirect(url_for('index'))
    customers = Customer.query.all()
    return render_template('edit_car.html', car=car, customers=customers)

@app.route('/delete_car/<int:id>', methods=['POST'])
def delete_car(id):
    car_to_delete = Car.query.get_or_404(id)
    db.session.delete(car_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
