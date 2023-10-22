from flask import Flask,render_template,url_for,redirect,request,flash
## create a simple flask application
from flask_sqlalchemy import SQLAlchemy  
import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Set the desired length of the random string
length_of_random_string = 10

# Generate the random string
random_string = generate_random_string(length_of_random_string)
print(random_string)


app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite3'  
app.config['SECRET_KEY'] = f"{random_string}"  

db = SQLAlchemy(app)  
  
class Employees(db.Model):  
   id = db.Column('employee_id', db.Integer, primary_key = True)  
   name = db.Column(db.String(100))  
   salary = db.Column(db.Float(50))  
   age = db.Column(db.String(200))   
   pin = db.Column(db.String(10))  
  
   def __init__(self, name, salary, age,pin):  
      self.name = name  
      self.salary = salary  
      self.age = age  
      self.pin = pin  
 
@app.route('/')  
def list_employees():  
   return render_template('list_employees.html', Employees = Employees.query.all() )  
 
@app.route('/add', methods = ['GET', 'POST'])  
def addEmployee():  
   if request.method == 'POST':  
      if not request.form['name'] or not request.form['salary'] or not request.form['age']:  
         flash('Please enter all the fields', 'error')  
      else:  
         employee = Employees(request.form['name'], request.form['salary'],  
            request.form['age'], request.form['pin'])  
           
         db.session.add(employee)  
         db.session.commit()  
         flash('Record was successfully added')  
         return redirect(url_for('list_employees'))  
   return render_template('add.html')  


 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()