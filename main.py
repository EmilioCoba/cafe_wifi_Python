from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)



class CafeForm(FlaskForm):
    name = StringField('Cafe name: ', validators=[DataRequired()])
    map_url= StringField('Google Maps (URL): ', validators=[DataRequired(),URL()])
    img_url= StringField('Image (URL): ', validators=[DataRequired(),URL()])
    location_name= StringField('Location name: ', validators=[DataRequired()])
    has_sockets=SelectField('Has charging sockets:',choices=[("1","yes"),("0","no")], validators=[DataRequired()])
    has_toilet=SelectField('Has toilet:',choices=[("1","yes"),("0","no")], validators=[DataRequired()])
    has_wifi=SelectField('Has wifi:',choices=[("1","yes"),("0","no")], validators=[DataRequired()])
    take_calls=SelectField('Can take calls:',choices=[("1","yes"),("0","no")], validators=[DataRequired()])
    seats=SelectField('Seats:',choices=[
        ("0-10", "0-10"),
        ("10-20", "10-20"),
        ("20-30", "20-30"),
        ("40-50", "40-50"),
        ("50+", "50+"),], validators=[DataRequired()])
    coffee_price= StringField('Coffee price: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Cafe(db.Model):
    __tablename__ = 'cafe'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str]= mapped_column(String(100))
    map_url:Mapped[str]= mapped_column(String(100))
    img_url:Mapped[str]= mapped_column(String(100))
    location:Mapped[str]= mapped_column(String(100))
    has_sockets:Mapped[int]= mapped_column(Integer)
    has_toilet:Mapped[int]= mapped_column(Integer)
    has_wifi:Mapped[int]= mapped_column(Integer)
    can_take_calls:Mapped[int]= mapped_column(Integer)
    seats:Mapped[str]= mapped_column(String)
    coffee_price:Mapped[str]= mapped_column(String)




@app.route("/")
def home():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("index.html", cafes=cafes)


@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe= Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location_name.data,
            has_sockets=int(form.has_sockets.data),
            has_toilet=int(form.has_toilet.data),
            has_wifi=int(form.has_wifi.data),
            can_take_calls=int(form.take_calls.data),
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html', form=form)


@app.route("/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe= db.get_or_404(Cafe, cafe_id)
    edit_form = CafeForm()

    if request.method == "GET":
        edit_form.name.data = cafe.name
        edit_form.map_url.data = cafe.map_url
        edit_form.img_url.data = cafe.img_url
        edit_form.location_name.data = cafe.location
        edit_form.has_sockets.data = str(cafe.has_sockets)
        edit_form.has_toilet.data = str(cafe.has_toilet)
        edit_form.has_wifi.data = str(cafe.has_wifi)
        edit_form.take_calls.data = str(cafe.can_take_calls)
        edit_form.seats.data = cafe.seats
        edit_form.coffee_price.data = cafe.coffee_price

    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location_name.data
        cafe.has_sockets = int(edit_form.has_sockets.data)
        cafe.has_toilet = int(edit_form.has_toilet.data)
        cafe.has_wifi = int(edit_form.has_wifi.data)
        cafe.can_take_calls = int(edit_form.take_calls.data)
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=edit_form,is_editing=True)

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
