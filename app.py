from flask import Flask , render_template,request,redirect,url_for,flash,session
from flask_session import Session
from flask_mail import Message
from flask_mail import Mail
from werkzeug.utils import secure_filename
from random import randint
from datetime import datetime
import os
import time
from flask_socketio import SocketIO, emit

# Ensure you have the necessary upload folder and allowed extensions defined
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask('app')
mail=Mail(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/uploads/img'

socketio = SocketIO(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='commerce4848@gmail.com'
app.config['MAIL_PASSWORD']='tcscpfzcklmxzgvw' #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


mail.init_app(app)
otp=randint(000000,999999)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
SESSION_TYPE='filesystem'
app.config.from_object(__name__)
Session(app)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size (16 MB)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        CustomerObj = Customer(email=email,password=password)
        AdminObj = Admin(email=email,password=password)
        TraderObj = Trader(email=email,password=password)

        success, cusId, message = CustomerObj.login()
        if success:
            session['emailUser'] = email
            session['idUser'] = cusId
            custList=CustomerObj.set_data()
            session['appUser'] = CustomerObj
            session['custList']=custList
            if custList[0]['status'] == 1 : 
                return " your Account Closed , Please Contact Admin !"
            else : 
                return redirect(url_for("home_page_with_login"))
        
        elif len(AdminObj.get_data()):
            session['emailUser'] = email
            session['idUser'] = cusId
            admList=AdminObj.set_data() 
            session['appUser'] = AdminObj
            session['admList']=admList
            if admList[0]['status'] == 1 : 
                return " your Account Closed , Please Contact Admin !"
            else :             
                return redirect(url_for("Home_admin"))
        
        elif len(TraderObj.get_data_trader()):
            # Store admin's email in session upon successful login
            session['emailUser'] = email
            session['idUser'] = cusId
            Traderlist=TraderObj.set_data() 
            session['appUser'] = TraderObj
            session['Traderlist']=Traderlist
            if Traderlist[0]['status'] == 1 : 
                return " your Account Closed , Please Contact Admin !"
            else :                
                return redirect(url_for("trader_homepage"))
        else:
            return render_template('login.html', error=message)
    else:
        return render_template('login.html')



#*************************************************#*************************************************#*************************************************
# Forget Password : OTP Verification
#*************************************************#*************************************************#*************************************************

@app.route('/verify', methods=[ "GET", "POST"])
def verify():
    if request.method == "POST":
        email = request.form['email']
        customerObj = Customer(email=email)
        otp , verification_otp = customerObj.send_verification_code()
        if otp :
            return render_template('verify.html', email=email , verification_otp = verification_otp)
        else:
            return render_template("enter_email_to_verify.html") + "Failed to send verification code."
    else : 
        return render_template("enter_email_to_verify.html")

#*************************************************
# Validate OTP before update password
#************************************************* 
@app.route('/validate', methods=['POST'])
def validate():
    if request.method == "POST":
        email = request.form['email']
        user_otp = request.form['otp']
        verification_otp = request.form['verification_otp']
        result, message = Customer.verify_otp(user_otp , verification_otp)
        #result, message = login_registration.verify_otp(email, user_otp)
        if result:
            return render_template('update_password.html', email=email)
        else:
            return message

#*************************************************
# Update Password
#************************************************* 
@app.route('/update_password', methods=['POST'])
def update_password():
    if request.method == "POST":
        email = request.form['email']
        new_password = request.form['password']
        customerObj = Customer(email=email)
        result, message = customerObj.updated_password(new_password)
        if result:
            return render_template('update_password.html') + "successful updated"
        else:
            return message
    else:
        return "Method Not Allowed"
#*************************************************#*************************************************#*************************************************
#*************************************************#*************************************************#*************************************************



#========================================================#========================================================#========================================================
# Student Page
#========================================================#========================================================#========================================================    
@app.route('/home_page_with_login')
def home_page_with_login():
# Retrieve customer email from session
    customer_data = session['custList']    
    if len(customer_data): 
    # Fetch category names and product counts from the database
      transobj = TransactionsWallet(user_id=customer_data[0]['id'] , type_user="customer")
      trans_data =transobj.show_transactions_typeuser() 
      Catobj = Category()
      Categories_count = Catobj.show_categories_with_product_count()
      print(f"Categories_count : {Categories_count}")
      products = Product()
      products = products.show_products()
      cartObj = Cart(customerId=customer_data[0]['id'])
      cart_data = cartObj.check_cart_data()
      WishObj = Wishlist(cmrId=customer_data[0]['id'])
      wishlist_data_exists = WishObj.check_wishlist_data()
      return render_template("Page_with_login.html" , trans_data = trans_data  , wishlist_data_exists = wishlist_data_exists, cart_data = cart_data, Categories_count=Categories_count, customer_data=customer_data[0], products=products)
    else:
# Handle the case where the customer with the provided email does not exist
      return "Customer not found", 404



