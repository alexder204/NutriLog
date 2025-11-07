from flask_sqlalchemy import SQLAlchemy

food_db = SQLAlchemy()

class Food(food_db.Model): # calories, total fat, protein, sugars, sodium, cholesterol, potassium, total carbohydrates
    def __init__(self, name, brand=None, calories=0, total_fat=0, protein=0, sugars=0, sodium=0, cholesterol=0, potassium=0, total_carbohydrates=0):
        super().__init__()
        self.name = name
        self.brand = brand
        self.calories = calories
        self.total_fat = total_fat
        self.protein = protein
        self.sugars = sugars
        self.sodium = sodium
        self.cholesterol = cholesterol
        self.potassium = potassium
        self.total_carbohydrates = total_carbohydrates

    __tablename__ = "food"

    id = food_db.Column(food_db.Integer, primary_key=True)
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

        existing_items = cls.query.filter_by(name=new_food.name, brand=new_food.brand).all()

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