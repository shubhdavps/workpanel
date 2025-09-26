from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Users and their dashboards
users = {
    "admin": {"password": "12345", "dashboard": "dashboard.html"},  # admin opens dashboard.html
    "manager": {"password": "54321", "dashboard": "manager_panel.html"},
    "staff": {"password": "1234567", "dashboard": "staff_panel.html"}
      
}

# Load leads from file if exists
def load_leads():
    if os.path.exists("leads.json"):
        with open("leads.json", "r") as f:
            return json.load(f)
    return []

# Save leads to file
def save_leads(leads):
    with open("leads.json", "w") as f:
        json.dump(leads, f)

# Initial load
leads = load_leads()

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username]["password"] == password:
        session['username'] = username
        session['dashboard'] = users[username]["dashboard"]
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid username or password!", "error")
        return redirect(url_for("index"))

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    global leads
    if 'username' not in session:
        return redirect(url_for("index"))

    # Admin lead form handling
    if session['username'] == 'admin' and request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        if name and email and phone:
            new_lead = {"name": name, "email": email, "phone": phone, "time": request.form.get("time")}
            leads.append(new_lead)
            save_leads(leads)  # Save to file
            flash(f"Lead {name} added successfully!", "success")
        else:
            flash("Please fill all fields!", "error")
        return redirect(url_for("dashboard"))

    return render_template(session['dashboard'], username=session['username'], leads=leads)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('dashboard', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

