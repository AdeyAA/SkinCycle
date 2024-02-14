app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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

@app.route("/", methods=["GET", "POST"])
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