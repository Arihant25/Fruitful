from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String(255), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.now)
    # completed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

# Used to create the database instance, comment after first run
# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['taskName']
        new_task = ToDo(taskName=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Oops! Some error occured."
    
    else:
        tasks = ToDo.query.order_by(ToDo.dateCreated).all()
        return render_template("index.html", tasks=tasks)
    
    # return render_template("index.html")


@app.route('/delete/<int:id>')
def delete(id):
    deleteTask = ToDo.query.get_or_404(id)

    try:
        db.session.delete(deleteTask)
        db.session.commit()
        return redirect('/')
    except:
        return "Oops! Some error occured."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    updateTask = ToDo.query.get_or_404(id)
    print(updateTask)

    if request.method == "POST":
        updateTask.taskName = request.form["taskName"]

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Oops! Some error occured."

    else:
        return render_template("update.html", task=updateTask)


if __name__ == "__main__":
    app.run(debug=True)
