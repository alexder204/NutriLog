from flask import Flask, render_template, request
from models import food_db, Food

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foods.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
food_db.init_app(app)

@app.route("/add_food", methods=["POST"])
def add_food():
    data = request.get_json()
    obj, removed = Food.add_or_replace(
        name=data["name"],
        brand=data.get("brand"),
        calories=data["calories"],
        total_fat=data["total_fat"],
        protein=data["protein"],
        sugars=data["sugars"],
        sodium=data["sodium"],
        cholesterol=data["cholesterol"],
        potassium=data["potassium"],
        total_carbohydrates=data["total_carbohydrates"],
    )
    return {"message": "Food saved", "replaced": removed, "id": obj.id}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        food_db.create_all()
    app.run(debug=True)
