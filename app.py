from flask import Flask, render_template, request, jsonify, session, redirect
from models import food_db, User, Food

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foods.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
food_db.init_app(app)

@app.route("/add_food", methods=["POST"])
def add_food():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()

    new_food = Food(
        user_id=session["user_id"],
        name=data["name"],
        brand=data.get("brand"),
        calories=data["calories"],
        total_fat=data["total_fat"],
        protein=data["protein"],
        sugars=data["sugars"],
        sodium=data["sodium"],
        cholesterol=data["cholesterol"],
        potassium=data["potassium"],
        total_carbohydrates=data["total_carbohydrates"]
    )

    food_db.session.add(new_food)
    food_db.session.commit()

    return jsonify({"message": "Food saved"})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        email=data["email"]
    )
    user.set_password(data["password"])

    food_db.session.add(user)
    food_db.session.commit()

    return jsonify({"message": "User created"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Logged in"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    with app.app_context():
        food_db.create_all()
    app.run(debug=True)
