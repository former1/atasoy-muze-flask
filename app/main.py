
from email.policy import default
from re import search
import re
from flask import Flask, render_template, request, redirect, url_for,flash, session
from flask_sqlalchemy import SQLAlchemy
import os 
from datetime import datetime
from werkzeug.utils import secure_filename
from base64 import b64encode
import base64
from io import BytesIO

DB_NAME ="eserlist.db"

app = Flask(__name__)
app.config['SECRET_KEY'] ="1991"
app.config['SQLALCHEMY_DATABASE_URI'] =f"sqlite:///{DB_NAME}"

  
ALLOWED_EXTENSION ={'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


db = SQLAlchemy(app)




class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    eserler = db.relationship('Eserler', backref='eserci')
    
    def __repr__(self):
        return self.name + " " +  self.surname


class Eserler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eser= db.Column(db.String(300), nullable=False)
    detail = db.Column(db.Text, nullable= False)
    eser_sahibi = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) 
    eserci_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    """
    data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
    rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser

    def __repr__(self):
          return f'Pic Name: {self.name} Data: {self.data}'

@app.before_first_request
def create_tables():
    db.create_all()



def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic
"""

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route("/")
def home():

    if 'email' in session:
        email = session['email']
        me = Users.query.filter_by(email=email).first()
        return render_template("home.html", me=me)

    return render_template("home.html")
    

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="POST":
        name =request.form.get('name')
        surname =request.form.get('surname')
        email =request.form.get('email')
        password =request.form.get('password')

            
        search = Users.query.filter_by(email=email).first()

        if search != None:
            flash('Bu email hesabı ile bir hesap zaten var')
            return render_template('register.html')
            
        new_user = Users(name=name, surname=surname,
                            email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("register.html")



@app.route("/login", methods=["GET","POST"])
def login():

    if 'email' in session:
        return redirect(url_for("home"))

    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        search = Users.query.filter_by(email=email).first()

        if search is None:
            flash("Hesap Bulunamadı")
            return render_template("login.html")

        if password == search.password:
            session["email"] = email
            return redirect(url_for("home"))

    return render_template("login.html")




"""
@app.route("/museum")
def museum():
    if 'email' in session:
        email = session['email']
        me = Users.query.filter_by(email=email).first()
        eserler = Eserler.query.all()
        return render_template("visitor.html", me=me,eserler=eserler)

    
    if 'email' not in session:
        eserler = Eserler.query.all()
        return render_template("visitor.html", eserler=eserler)


"""


@app.route("/logout")
def logout():
    session.pop("email",None)
    return redirect(url_for("home"))





""""
    file = request.files['inputFile']
    rs_username = request.form['txtusername']
    filename = secure_filename(file.filename)
  
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  
       newFile = User(profile_pic=file.filename, username=rs_username, email='Ednalan@gmail.com')
       db.session.add(newFile)
       db.session.commit()
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       return redirect('/')
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
    return redirect('/')    
"""

@app.route("/create",methods=["GET","POST"])
def create():

    if 'email' in session:
        email = session["email"]
        me = Users.query.filter_by(email=email).first()

        if request.method == "POST":
            eser = request.form.get("eser")
            detail = request.form.get("detail")
            eser_sahibi = request.form.get("eser_sahibi")
            



            """

            file = request.files['inputFile']
            data = file.read()
            render_file = render_picture(data)
"""
            new_eser=Eserler(eser=eser, detail=detail,
                             eser_sahibi=eser_sahibi, eserci_id = me.id)

            db.session.add(new_eser)
            db.session.commit()
            return redirect(url_for("home"))


    return render_template("create.html")




@app.route("/visitor")
def visitor():
    if 'email' in session:
        email = session['email']
        me = Users.query.filter_by(email=email).first()
        eserler = Eserler.query.all()
        return render_template("visitor.html", me=me,eserler=eserler)

    
    if 'email' not in session:
        eserler = Eserler.query.all()
        return render_template("visitor.html", eserler=eserler)


@app.route("/galeri")
def galeri():
    return render_template("galeri.html")


@app.route("/howtogo")
def howtogo():
    return render_template("howtogo.html")



@app.route("/about_sait")
def about_sait():
    return render_template("about_sait.html")


@app.route("/about_muze")
def about_muze():
    return render_template("about_muze.html")



@app.route("/hours")
def hours():
    return render_template("hours.html")


@app.route("/bolgeler")
def bolgeler():
    return render_template("bolgeler.html")







"""Müzelere ait sayfaların direction kodları"""

"""Sait Faik"""

@app.route("/sait_faik_museum")
def sait_faik_museum():
    return render_template("sait_faik_museum.html")


@app.route("/sait_faik_howtogo")
def sait_faik_howtogo():
    return render_template("sait_faik_howtogo.html")


@app.route("/sait_faik_galeri")
def sait_faik_galeri():
    return render_template("sait_faik_galeri.html")


@app.route("/sait_faik_hours")
def sait_faik_hours():
    return render_template("sait_faik_hours.html")


@app.route("/about_sait_faik")
def about_sait_faik():
    return render_template("about_sait_faik.html")


@app.route("/about_sait_faik_muze")
def about_sait_faik_muze():
    return render_template("about_sait_faik_muze.html")










"""Cahit Sıtkı Tarancı"""

@app.route("/cahit_sıtkı_museum")
def cahit_sıtkı_museum():
    return render_template("cahit_sıtkı_museum.html")


@app.route("/cahit_sıtkı_howtogo")
def cahit_sıtkı_howtogo():
    return render_template("cahit_sıtkı_howtogo.html")


@app.route("/cahit_sıtkı_galeri")
def cahit_sıtkı_galeri():
    return render_template("cahit_sıtkı_galeri.html")


@app.route("/cahit_sıtkı_hours")
def cahit_sıtkı_hours():
    return render_template("cahit_sıtkı_hours.html")


@app.route("/about_cahit_sıtkı")
def about_cahit_sıtkı():
    return render_template("about_cahit_sıtkı.html")


@app.route("/about_cahit_sıtkı_muze")
def about_cahit_sıtkı_muze():
    return render_template("about_cahit_sıtkı_muze.html")








"""Mehmet Akif Ersoy"""

@app.route("/mehmet_akif_museum")
def mehmet_akif_museum():
    return render_template("mehmet_akif_museum.html")


@app.route("/mehmet_akif_howtogo")
def mehmet_akif_howtogo():
    return render_template("mehmet_akif_howtogo.html")


@app.route("/mehmet_akif_galeri")
def mehmet_akif_galeri():
    return render_template("mehmet_akif_galeri.html")


@app.route("/mehmet_akif_hours")
def mehmet_akif_hours():
    return render_template("mehmet_akif_hours.html")


@app.route("/about_mehmet_akif")
def about_mehmet_akif():
    return render_template("about_mehmet_akif.html")


@app.route("/about_mehmet_akif_muze")
def about_mehmet_akif_muze():
    return render_template("about_mehmet_akif_muze.html")






if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        db.create_all(app=app)
        print("Database Oluşturuldu")

    app.debug = True
    app.run()


