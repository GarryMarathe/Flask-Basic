from flask import Flask ,render_template,request,redirect,flash,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/AI"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)



@app.route("/start")
def intro():
    return "<p>Hello, World!</p>"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# @app.route("/dashboard", methods=["GET", "POST"])
# def dashboard():
#     return render_template("dashboard.html")

# @app.route("/add_article",method=["GET","POST"])
# def add_article():
#     return

@app.route("/login", methods=["GET", "POST"])
def login():
    # bussiness logic
    if request.method == "POST":
        # accept data from frontend(form data) - > email and password
        email = request.form["email"]
        password = request.form["password"]

        # Check if that email is present in database or not
        found_user = mongo.db.users.find_one({"email": email})
        # print(found_user)
        if found_user:
            print("user found")
            # if email is present then compare password_hash from db with user's entered password
            is_password_matched = bcrypt.check_password_hash(
                found_user["password"], password
            )

            if is_password_matched:
                print("correct password")
                # if password also matched then login successfull and redirect to dashboard
                session["is_user_logged_in"] = True
                session["first_name"] = found_user["first_name"]
                session["last_name"] = found_user["last_name"]
                session["email"] = found_user["email"]
                flash("Login successfull", "success")
                return redirect("/dashboard")
            else:
                print("incorrect password")
                flash("Invalid password provided", "danger")    

        else:
            print("no user found")
            flash("User not registered", "danger")

    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():

    #business logic
    if request.method == "POST":
        print("it's a post call")
        
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        city = request.form["city"]

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

      #  print(first_name)
      # print(last_name)
      # print(email)
      # print(password)
      #  print(address)
      #  print(phone_number)
      #  print(city)


        mongo.db.article.insert_one(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password_hash,
                "phone_number": phone_number,
                "address": address,
                "city": city,
            }
        )

     #   print(first_name,last_name, email_id, password,address,city)
    
    
        flash("User registered succesfully", "success")
        return redirect("/login")

    return render_template("signup.html")

    print("it's a get call")

if __name__=="__main__":
    app.secret_key = "asdkjssd"
    app.run(debug=True)