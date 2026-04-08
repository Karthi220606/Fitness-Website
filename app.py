from flask import Flask, render_template, request, jsonify, redirect, url_for
import os, json, datetime

APP_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(APP_DIR, "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        default = {
            "users": [
                {"username":"user1","password":"pass1","role":"user"},
                {"username":"admin","password":"admin123","role":"admin"}
            ],
            "calorie_entries": [],  # {username, date, calories, notes}
            "store_items": [
                {"id":1,"name":"Whey Protein","price":29.99,"desc":"Protein powder 2lb"},
                {"id":2,"name":"Yoga Mat","price":19.99,"desc":"Non-slip mat"}
            ],
            "workouts": {
                "legs":[
                    {"title":"Leg Day 1","youtube":"https://www.youtube.com/embed/UBMk30rjy0o"},
                    {"title":"Leg Workout at Home","youtube":"https://www.youtube.com/embed/2tM1LFFxeKg"}
                ],
                "shoulder":[
                    {"title":"Shoulder Strength","youtube":"https://www.youtube.com/embed/0l7T9kRrS0k"}
                ],
                "chest":[
                    {"title":"Chest Pump","youtube":"https://www.youtube.com/embed/IoXQ9b9tM6Y"}
                ]
            }
        }
        with open(DATA_FILE,"w") as f:
            json.dump(default,f,indent=2)
        return default
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE,"w") as f:
        json.dump(d,f,indent=2)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_user")
def login_user():
    return render_template("login_user.html")

@app.route("/login_admin")
def login_admin():
    return render_template("login_admin.html")

@app.route("/bmi")
def bmi():
    return render_template("bmi.html")

@app.route("/calorie_finder")
def calorie_finder():
    return render_template("calorie_finder.html")

@app.route("/calorie_tracker")
def calorie_tracker():
    return render_template("calorie_tracker.html")

@app.route("/diet_planner")
def diet_planner():
    return render_template("diet_planner.html")

@app.route("/workout_splits")
def workout_splits():
    return render_template("workout_splits.html")

@app.route("/workouts/<section>")
def workouts(section):
    data = load_data()
    workouts = data.get("workouts", {}).get(section, [])
    return render_template("workouts.html", section=section, workouts=workouts)

@app.route("/store")
def store():
    data = load_data()
    return render_template("store.html", items=data.get("store_items",[]))

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# API endpoints
@app.route("/api/login", methods=["POST"])
def api_login():
    body = request.json
    username = body.get("username")
    password = body.get("password")
    data = load_data()
    for u in data.get("users",[]):
        if u["username"] == username and u["password"] == password:
            return jsonify({"ok":True,"username":username,"role":u.get("role","user")})
    return jsonify({"ok":False,"error":"Invalid credentials"}), 401

@app.route("/api/calorie_entry", methods=["GET","POST"])
def api_calorie_entry():
    data = load_data()
    if request.method == "POST":
        body = request.json
        entry = {
            "username": body.get("username","guest"),
            "date": body.get("date", datetime.date.today().isoformat()),
            "calories": body.get("calories",0),
            "notes": body.get("notes","")
        }
        data.setdefault("calorie_entries",[]).append(entry)
        save_data(data)
        return jsonify({"ok":True,"entry":entry})
    else:
        username = request.args.get("username")
        entries = data.get("calorie_entries",[])
        if username:
            entries = [e for e in entries if e.get("username")==username]
        return jsonify({"ok":True,"entries":entries})

@app.route("/api/store/buy", methods=["POST"])
def api_store_buy():
    body = request.json
    item_id = int(body.get("id",0))
    data = load_data()
    item = next((i for i in data.get("store_items",[]) if i["id"]==item_id), None)
    if not item:
        return jsonify({"ok":False,"error":"Item not found"}), 404
    # Simulate purchase (no payment)
    return jsonify({"ok":True,"message":f"Purchased {item['name']}"})

@app.route("/api/workouts")
def api_workouts():
    data = load_data()
    return jsonify({"ok":True,"workouts":data.get("workouts",{})})

if __name__ == "__main__":
    app.run(debug=True)
