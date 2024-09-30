from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/hotel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model definitions
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String, nullable=False)
    customer_address = db.Column(db.String, nullable=False)
    customer_dob = db.Column(db.Date, nullable=False)
    customer_age = db.Column(db.Integer, nullable=False)
    customer_mobile_no = db.Column(db.String, nullable=False)

class Room(db.Model):
    room_no = db.Column(db.Integer, primary_key=True)
    room_rates = db.Column(db.Integer, nullable=False)
    room_status = db.Column(db.String, nullable=False)  # Adjust this according to your ENUM

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String, nullable=False)
    employee_address = db.Column(db.String, nullable=False)
    employee_mobile_no = db.Column(db.String, nullable=False)
    employee_job_desc = db.Column(db.String, nullable=False)  # Added job description field

@app.route('/')
def index():
    return redirect(url_for('home'))  # Redirect to the home page

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/customers')
def customers():
    customers = Customer.query.all()  # Fetch all customers
    return render_template('customers.html', customers=customers)

@app.route('/rooms')
def rooms():
    rooms = Room.query.all()  # Fetch all rooms
    return render_template('rooms.html', rooms=rooms)

@app.route('/employees')
def employees():
    employees = Employee.query.all()  # Fetch all employees
    return render_template('employees.html', employees=employees)

# Add Customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_address = request.form['customer_address']
        customer_dob = request.form['customer_dob']
        customer_age = request.form['customer_age']
        customer_mobile_no = request.form.get('customer_mobile_no')

        # Input validation
        if not customer_name or not customer_address or not customer_dob or not customer_age or not customer_mobile_no:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_customer'))

        try:
            customer_dob = datetime.strptime(customer_dob, '%Y-%m-%d').date()  # Ensure the date format is correct
            customer_age = int(customer_age)  # Convert age to integer
        except ValueError:
            flash('Invalid input for date or age!', 'error')
            return redirect(url_for('add_customer'))

        new_customer = Customer(
            customer_name=customer_name,
            customer_address=customer_address,
            customer_dob=customer_dob,
            customer_age=customer_age,
            customer_mobile_no=customer_mobile_no
        )
        
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')  # Success message
        return redirect(url_for('add_customer'))  # Redirect to the same page after adding

    return render_template('add_customer.html')

# Add Room
@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_no = request.form['room_no']
        room_rates = request.form['room_rates']
        room_status = request.form['room_status']

        # Input validation
        if not room_no or not room_rates or not room_status:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_room'))

        new_room = Room(
            room_no=room_no,
            room_rates=room_rates,
            room_status=room_status
        )
        
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('add_room'))

    return render_template('add_room.html')

# Add Employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        employee_address = request.form['employee_address']
        employee_mobile_no = request.form['employee_mobile_no']
        employee_job_desc = request.form['employee_job_desc']

        # Input validation
        if not employee_name or not employee_address or not employee_mobile_no or not employee_job_desc:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_employee'))

        new_employee = Employee(
            employee_name=employee_name,
            employee_address=employee_address,
            employee_mobile_no=employee_mobile_no,
            employee_job_desc=employee_job_desc
        )
        
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')  # Success message
        return redirect(url_for('add_employee'))  # Redirect to the same page after adding

    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True)
