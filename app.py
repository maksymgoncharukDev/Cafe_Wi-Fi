from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)

# Database setup
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Cafe Table Model
class Cafe(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(250), unique=True, nullable=False)
    map_url = mapped_column(String(500), nullable=False)
    img_url = mapped_column(String(500), nullable=False)
    location = mapped_column(String(250), nullable=False)
    seats = mapped_column(String(250), nullable=False)
    has_toilet = mapped_column(Boolean, nullable=False)
    has_wifi = mapped_column(Boolean, nullable=False)
    has_sockets = mapped_column(Boolean, nullable=False)
    can_take_calls = mapped_column(Boolean, nullable=False)
    coffee_price = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    cafes = Cafe.query.all()  # Get all cafes from the database
    return render_template("index.html", cafes=cafes)  # Pass cafes to the template

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=request.form.get("has_toilet") == 'on',
            has_wifi=request.form.get("has_wifi") == 'on',
            has_sockets=request.form.get("has_sockets") == 'on',
            can_take_calls=request.form.get("can_take_calls") == 'on',
            coffee_price=request.form.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_cafe.html")

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update-price/<int:cafe_id>", methods=["GET", "POST"])
def update_price(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    if request.method == "POST":
        new_price = request.form.get("new_price")
        cafe.coffee_price = new_price
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("update_price.html", cafe=cafe)

if __name__ == '__main__':
    app.run(debug=True)