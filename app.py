from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from sklearn.linear_model import LinearRegression
from sqlalchemy import extract
import csv
from io import StringIO
from statistics import mean, stdev

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///acadescore.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

model = joblib.load("Random_Forest.pkl")

# ---------------- DATABASE MODELS ----------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    study_hours = db.Column(db.Float)
    social_media = db.Column(db.Float)
    part_time_job = db.Column(db.Integer)
    attendance = db.Column(db.Float)
    sleep = db.Column(db.Float)
    mental_health = db.Column(db.Float)

    score = db.Column(db.Float)

    entry_date = db.Column(db.Date, nullable=False)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- AUTH ----------------

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if not user:
            error = "Account does not exist. Please register."
        elif not check_password_hash(user.password, request.form["password"]):
            error = "Incorrect password."
        else:
            login_user(user)
            return redirect("/dashboard")

    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        existing = User.query.filter_by(email=request.form["email"]).first()
        if existing:
            error = "Email already registered."
        else:
            hashed = generate_password_hash(request.form["password"])
            user = User(email=request.form["email"], password=hashed)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")

    return render_template("register.html", error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# ---------------- DATA ENTRY ----------------
@app.route("/data-entry", methods=["GET", "POST"])
@login_required
def data_entry():

    if request.method == "POST":

        # Get selected date
        entry_date = datetime.strptime(
            request.form["entry_date"],
            "%Y-%m-%d"
        ).date()

        # Prevent future date
        if entry_date > date.today():
            return render_template(
                "data_entry.html",
                error="Future dates are not allowed.",
                today=date.today()
            )

        # Check duplicate entry for same date
        existing_entry = Prediction.query.filter_by(
            user_id=current_user.id,
            entry_date=entry_date
        ).first()

        if existing_entry:
            return render_template(
                "data_entry.html",
                error="Entry already exists for selected date.",
                today=date.today()
            )

        # Prepare ML input (ONLY 6 FEATURES)
        input_df = pd.DataFrame([{
            "study_hours_per_day": float(request.form["study_hours"]),
            "social_media_hours": float(request.form["social_media"]),
            "part_time_job": int(request.form["part_time_job"]),
            "attendance_percentage": float(request.form["attendance"]),
            "sleep_hours": float(request.form["sleep"]),
            "mental_health_rating": float(request.form["mental_health"])
        }])

        predicted_score = model.predict(input_df)[0]

        # Save to database
        new_entry = Prediction(
            user_id=current_user.id,
            study_hours=float(request.form["study_hours"]),
            social_media=float(request.form["social_media"]),
            part_time_job=int(request.form["part_time_job"]),
            attendance=float(request.form["attendance"]),
            sleep=float(request.form["sleep"]),
            mental_health=float(request.form["mental_health"]),
            score=predicted_score,
            entry_date=entry_date
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "data_entry.html",
        today=date.today()
    )
# ---------------- DASHBOARD ----------------


@app.route("/dashboard")
@login_required
def dashboard():

    # Get all entries sorted by date
    entries = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(Prediction.entry_date.asc()).all()

    # Latest entry
    latest = entries[-1] if entries else None

    # Prepare graph data
    scores = [round(e.score, 2) for e in entries]
    dates = [e.entry_date.strftime("%d %b") for e in entries]

    # =============================
    # PERFORMANCE METRICS
    # =============================

    # Last performance
    last_performance = round(latest.score, 2) if latest else 0

    # Weekly average
    week_entries = [
        e.score for e in entries
        if e.entry_date >= date.today() - timedelta(days=7)
    ]

    weekly_avg = round(
        sum(week_entries)/len(week_entries), 2
    ) if week_entries else 0


    # Monthly average
    month_entries = [
        e.score for e in entries
        if e.entry_date >= date.today() - timedelta(days=30)
    ]

    monthly_avg = round(
        sum(month_entries)/len(month_entries), 2
    ) if month_entries else 0


    # =============================
    # CONSISTENCY SCORE
    # =============================

            # Consistency calculation
    # Consistency Score (correct and stable)
    if len(scores) > 1:
        std = np.std(scores)
        consistency = round(max(0, 100 - std), 2)
    else:
        consistency = 100 if scores else 0

    # =============================
    # IMPROVEMENT TRACKER
    # =============================

    study_improvement = 0
    attendance_improvement = 0
    sleep_improvement = 0
    mental_improvement = 0

    if len(entries) >= 2:

        prev = entries[-2]
        curr = entries[-1]

        study_improvement = round(
            curr.study_hours - prev.study_hours, 2
        )

        attendance_improvement = round(
            curr.attendance - prev.attendance, 2
        )

        sleep_improvement = round(
            curr.sleep - prev.sleep, 2
        )

        mental_improvement = round(
            curr.mental_health - prev.mental_health, 2
        )


    # =============================
    # WHAT IMPROVED
    # =============================

    improvements = []

    if study_improvement > 0:
        improvements.append("Study hours improved")

    if attendance_improvement > 0:
        improvements.append("Attendance improved")

    if sleep_improvement > 0:
        improvements.append("Sleep improved")

    if mental_improvement > 0:
        improvements.append("Mental health improved")


    # =============================
    # SUGGESTIONS
    # =============================

    suggestions = []

    if latest:

        if latest.study_hours < 4:
            suggestions.append("Increase study hours")

        if latest.attendance < 75:
            suggestions.append("Improve attendance")

        if latest.sleep < 6:
            suggestions.append("Sleep more for better performance")

        if latest.mental_health < 6:
            suggestions.append("Improve mental wellness")

        if latest.social_media > 5:
            suggestions.append("Reduce social media usage")


    # =============================
    # FEATURE IMPORTANCE (STATIC)
    # =============================

    importance = [35, 15, 10, 20, 10, 10]


    # =============================
    # RENDER DASHBOARD
    # =============================

    return render_template(

        "dashboard.html",

        latest=latest,

        last_performance=last_performance,
        weekly_avg=weekly_avg,
        monthly_avg=monthly_avg,

        consistency=consistency,

        scores=scores,
        dates=dates,

        importance=importance,

        study_improvement=study_improvement,
        attendance_improvement=attendance_improvement,
        sleep_improvement=sleep_improvement,
        mental_improvement=mental_improvement,

        suggestions=suggestions,
        improvements=improvements

    )
    
@app.route("/history")
@login_required
def history():

    page = request.args.get("page", 1, type=int)
    selected_month = request.args.get("month")

    query = Prediction.query.filter_by(user_id=current_user.id)

    if selected_month and selected_month != "":
        query = query.filter(
            extract('month', Prediction.entry_date) == int(selected_month)
        )

    pagination = query.order_by(
        Prediction.entry_date.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    entries = pagination.items

    return render_template(
        "history.html",
        entries=entries,
        page=pagination.page,
        total_pages=pagination.pages,
        selected_month=selected_month
    )
    
@app.route("/delete/<int:id>")
@login_required
def delete_entry(id):

    entry = Prediction.query.get_or_404(id)

    if entry.user_id != current_user.id:
        return "Unauthorized"

    db.session.delete(entry)
    db.session.commit()

    return redirect("/history")

@app.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit_entry(id):

    entry = Prediction.query.get_or_404(id)

    if entry.user_id != current_user.id:
        return "Unauthorized"

    if request.method == "POST":

        entry.study_hours = float(request.form["study"])
        entry.social_media = float(request.form["social"])
        entry.attendance = float(request.form["attendance"])
        entry.sleep = float(request.form["sleep"])
        entry.mental_health = float(request.form["mental"])

        # Recalculate prediction
        input_df = pd.DataFrame([{
            "study_hours_per_day": entry.study_hours,
            "social_media_hours": entry.social_media,
            "part_time_job": entry.part_time_job,
            "attendance_percentage": entry.attendance,
            "sleep_hours": entry.sleep,
            "mental_health_rating": entry.mental_health
        }])

        entry.score = model.predict(input_df)[0]

        db.session.commit()

        return redirect("/history")

    return render_template("edit.html", entry=entry)

@app.route("/export")
@login_required
def export_csv():

    entries = Prediction.query.filter_by(
        user_id=current_user.id
    ).all()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Date","Study","Social","Attendance","Sleep","Mental","Score"])

    for e in entries:
        writer.writerow([
            e.entry_date.strftime("%d-%m-%Y"),
            e.study_hours,
            e.social_media,
            e.attendance,
            e.sleep,
            e.mental_health,
            e.score
        ])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-type"] = "text/csv"

    return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)