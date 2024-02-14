from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    skincare = db.relationship('Skincare', backref='user', lazy=True)


class SkinCare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_of_day = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    feedback = db.Column(db.String(20), nullable=False, default='default_feedback')

    def __repr__(self):
        return f"<Skincare: {self.name}, {self.time_of_day}, {self.category}, {self.feedback}>"

with app.app_context():
    db.create_all()

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/", methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        new_skincare_info = SkinCare(
            name=request.form["skincare_name"],
            time_of_day=request.form["selected_day"],
            category=request.form["selected_category"],
            feedback="default_feedback"
        )
        db.session.add(new_skincare_info)
        db.session.commit()
        return redirect(url_for("main"))

    return render_template("index.html")

@app.route("/summary")
def summary():
    skincare_records = SkinCare.query.all()
    morning_records = [record for record in skincare_records if record.time_of_day == 'Morning Routine']
    night_records = [record for record in skincare_records if record.time_of_day == 'NightTime Routine']

    return render_template("summary.html", morning_summary=morning_records, night_summary=night_records)

@app.route("/feedback/<int:id>", methods=["POST"])
def feedback(id):
    skincare_info = SkinCare.query.get_or_404(id)
    action = request.form["action"]

    if action == "like":
        skincare_info.feedback = "liked"
    elif action == "dislike":
        skincare_info.feedback = "disliked"
    else:
        skincare_info.feedback = "unknown"

    db.session.commit()
    return redirect(url_for("summary"))

@app.route("/remove_skincare", methods=["POST"])
def remove_skincare():
    id = request.form.get('id')
    routine = request.form.get('routine')
    skincare_item = SkinCare.query.get(id)
    db.session.delete(skincare_item)
    db.session.commit()
    return redirect(url_for('summary'))

if __name__ == "__main__":
    app.run(debug=True)