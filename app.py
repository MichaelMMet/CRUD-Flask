#Import
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#My application

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TaskDB.db"
db = SQLAlchemy(app)

#Data class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"

#Home page
@app.route("/", methods=["POST", "GET"])
def index():
    #Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
#See all current tasks
    else: 
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)



if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)