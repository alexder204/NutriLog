from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

food_db = SQLAlchemy()

class User(food_db.Model):
    __tablename__ = "user"

    id = food_db.Column(food_db.Integer, primary_key=True)
    username = food_db.Column(food_db.String(80), unique=True, nullable=False)
    email = food_db.Column(food_db.String(255), unique=True)
    password_hash = food_db.Column(food_db.String(200), nullable=False)

    foods = food_db.relationship("Food", backref="owner", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Food(food_db.Model):
    __tablename__ = "food"

    id = food_db.Column(food_db.Integer, primary_key=True)
    user_id = food_db.Column(food_db.Integer, food_db.ForeignKey("user.id"), nullable=False)
    name = food_db.Column(food_db.String(255), nullable=False)
    brand = food_db.Column(food_db.String(255))
    calories = food_db.Column(food_db.Float, nullable=False)
    total_fat = food_db.Column(food_db.Float, default=0)
    protein = food_db.Column(food_db.Float, default=0)
    sugars = food_db.Column(food_db.Float, default=0)
    sodium = food_db.Column(food_db.Float, default=0)
    cholesterol = food_db.Column(food_db.Float, default=0)
    potassium = food_db.Column(food_db.Float, default=0)
    total_carbohydrates = food_db.Column(food_db.Float, default=0)

    def duplicate(self, other) -> bool:
        if self.name != other.name or self.brand != other.brand:
            return False
        
        numeric_fields = ["calories", "total_fat", "protein", "sugars",
        "sodium", "cholesterol", "potassium", "total_carbohydrates"]

        for field in numeric_fields:
            value1 = getattr(self, field) or 0.0
            value2 = getattr(other, field) or 0.0

            if abs(value1 - value2) > 0.01:
                return False

        return True
    
    @classmethod
    def add_or_replace(cls, **data):
        data["name"] = data["name"].strip()
        data["brand"] = data.get("brand") or None

        numeric_fields = ["calories", "total_fat", "protein", "sugars",
            "sodium", "cholesterol", "potassium", "total_carbohydrates"]
        for field in numeric_fields:
            if field in data and data[field] is not None:
                data[field] = float(data[field])

        new_food = cls(**data)

        existing_items = cls.query.filter_by(user_id=new_food.user_id, name=new_food.name, brand=new_food.brand).all()

        removed_count = 0
        for item in existing_items:
            if item.duplicate(new_food):
                food_db.session.delete(item)
                removed_count += 1

        food_db.session.flush()
        food_db.session.add(new_food)
        food_db.session.commit()

        return new_food, removed_count


    def __repr__(self):
        return f"<Food {self.name} ({self.calories} cal)>"