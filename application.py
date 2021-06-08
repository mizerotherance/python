from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flask_db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class students(db.Model):

    _tablename_ = 'students'

    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    class_id = db.Column(db.Integer, db.ForeignKey(
        'classes.id'), nullable=False)


def __init__(self, name, city, addr, pin):
    self.name = name
    self.city = city
    self.addr = addr
    self.pin = pin


def __repr__(self):
    return f'<students: {self.id} {self.name}>'


class classes(db.Model):

    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    student_id = db.relationship('students', backref='classes', lazy=True)

    def __repr__(self):
        return f'<classes: {self.id}>'


@app.route('/')
def home():
    schools = students.query.all()
    return render_template('home.html', schools=schools, classes=classes.query.all())


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            schools = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(schools)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('about'))
    return render_template('about.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
