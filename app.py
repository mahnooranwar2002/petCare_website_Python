
from flask import Flask,render_template,session,request, redirect,url_for

import mysql.connector
import matplotlib.pyplot as plt
import plotly.graph_objs as go
app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(32)


# -------------------------------------------Wesbite Api------------------------------------------- 

def getDb():
     return mysql.connector.connect(
         host="localhost",
        user="root",
        password="",
          database="db_pet"
     )
@app.route("/")
def hello_world():
    if 'sid' not in session:
        return render_template("website/index.html",user=None)

    con = getDb()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM `users` WHERE id = %s", (session['sid'],))
       
        user = cursor.fetchone()

        con.close()

        return render_template("website/index.html", user=user, )

    except Exception as e:
        print(f"An error occurred: {e}")
        con.close()
        return "An error occurred"

      


@app.route("/about")
def about():
       
          if 'sid' not in session:
            return render_template("website/about.html",user=None)
          
          con = getDb()
          cursor=con.cursor(dictionary=True)
          cursor.execute("SELECT * FROM `services`")
          service = cursor.fetchall()

          cursor.execute("SELECT * FROM `users` where id = %s",(session['sid'],))
          # cursor.execute("SELECT * FROM `users` where id = %s ",(['sid'],))
         
          user = cursor.fetchone()
          con.close()
          return render_template("website/about.html",user=user)
      
     
@app.route("/contact")
def contact():
          if 'sid' not in session:
            return render_template("website/contact.html",user=None)
          
          con = getDb()
          cursor=con.cursor(dictionary=True)
         

          cursor.execute("SELECT * FROM `users` where id = %s",(session['sid'],))
          # cursor.execute("SELECT * FROM `users` where id = %s ",(['sid'],))
         
          user = cursor.fetchone()
          con.close()
          return render_template("website/contact.html",user=user)
  
@app.route("/Addcontact",methods=["post"])
def contactAdd():
     name = request.form["name"]
     email = request.form["email"]
     sub = request.form["sub"]
     msg = request.form["msg"]
      
     con=getDb()
     cursor= con.cursor()
     cursor.execute("INSERT INTO `contact`( `name`, `email`, `sub`, `msg`) VALUES (%s,%s,%s,%s)",(name,email,sub,msg))
     con.commit()
     con.close()
     return redirect(url_for('contact'))
# if 'sid' not in session:
#         return redirect(url_for('loginuser'))
#     return render_template("dashboard.html")
@app.route("/appointment")
def appointment():
          if 'sid' not in session:
              return redirect(url_for('login'))
          
          con = getDb()
          cursor=con.cursor(dictionary=True)
          cursor.execute("SELECT * FROM `services`")
          service = cursor.fetchall()

          cursor.execute("SELECT * FROM `users` where id = %s",(session['sid'],))
          # cursor.execute("SELECT * FROM `users` where id = %s ",(['sid'],))
         
          user = cursor.fetchone()
          con.close()
          return render_template("website/appointment.html",service=service,user=user)
    


@app.route("/login")
def login():
     return render_template("website/login.html")

@app.route('/loginuser', methods=['GET', 'POST'])
def logined():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        con = getDb()
        cursor = con.cursor(dictionary=True)
        # Database check (plain text comparison - INSECURE)
        cursor.execute("SELECT * FROM users WHERE email= %s AND pass=%s AND status = %s And is_admin = %s ", (email, password,1,0))
        user = cursor.fetchone()
        
        if user:
            session['sid'] = user['id']  # Set session
            session.permanent = True  # Optional: make persistent
            return redirect(url_for('hello_world'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        con = getDb()
        cursor = con.cursor(dictionary=True)
        # Database check (plain text comparison - INSECURE)
        cursor.execute("SELECT * FROM users WHERE email= %s AND pass=%s AND status = %s And is_admin = %s", (email, password,1,1))
        user = cursor.fetchone()
        
        if user:
            session['adminSession'] = user['id']  # Set session
            session.permanent = True  # Optional: make persistent
            return redirect(url_for('Dashboard'))



@app.route("/logout")
def logout():
      session.clear()
      return redirect(url_for("hello_world"))

@app.route("/appointmentbooked")
def appointmentbookeds():
          if 'sid' not in session:
              return redirect(url_for('login'))
          
          con = getDb()
          cursor=con.cursor(dictionary=True)
          cursor.execute("""
        SELECT a.*, s_name as service_name
        FROM `appointment` a
        JOIN `services` s ON a.service_id = s.id  where user_id = %s
        """ ,(session['sid'],))
          appointment = cursor.fetchall() 
        #   cursor.execute("SELECT * FROM `appointment` where user_id =%s",(session['sid'],))
        #   appointment = cursor.fetchall()

          cursor.execute("SELECT * FROM `users` where id = %s",(session['sid'],))
          # cursor.execute("SELECT * FROM `users` where id = %s ",(['sid'],))
         
          user = cursor.fetchone()

          con.close()
          return render_template("website/booked_appoinment.html",appointment=appointment,user=user)
        

@app.route("/registered")
def registered():
     return render_template("website/registered.html")

# for register a user
@app.route("/userResgitered",methods=["post"])
def registereduser():
     name= request.form["name"]
     email= request.form["email"]
     password= request.form["pass"]
     status=1
     is_admin=0
     con=getDb()
     cursor= con.cursor()
     cursor.execute("INSERT INTO `users`( `name`, `email`, `pass`, `status`, `is_admin`) VALUES (%s,%s,%s,%s,%s)",(name,email,password,status,is_admin))
     con.commit()
     con.close()
     return render_template("website/registered.html")


# for booking service

@app.route("/bookingAppointment" , methods = ["post"])
def appointmentbooked():
       name = request.form["u_name"]
       u_id = request.form["u_id"]
       app_date = request.form["app_date"]
       app_time = request.form["app_time"]
       service = request.form["service"]
       msg=request.form["msg"]
       status="pending"
       con = getDb()
       cursor=con.cursor()
       cursor.execute("INSERT INTO `appointment`( `user_name`, `user_id`, `app_date`, `app_time`, `msg`, `service_id`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name,u_id,app_date,app_time,msg,service,status))
       con.commit()
       con.close()
       return redirect(url_for('appointment'))

@app.route("/profile")
def profile():
          if 'sid' not in session:
              return redirect(url_for('login'))
          
          con = getDb()
          cursor=con.cursor(dictionary=True)
          cursor.execute("SELECT * FROM `appointment` where user_id =%s",(session['sid'],))
          appointment = cursor.fetchall()

          cursor.execute("SELECT * FROM `users` where id = %s",(session['sid'],))
          # cursor.execute("SELECT * FROM `users` where id = %s ",(['sid'],))
         
          user = cursor.fetchone()

          con.close()
          return render_template("website/profile.html",appointment=appointment,user=user)

@app.route("/userUpdate", methods=["POST"])
def udateProfile():
    if 'sid' not in session:
        return redirect(url_for('login'))

    con = getDb()
    cursor = con.cursor()

    try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]

        cursor.execute("UPDATE `users` SET `name` = %s, `email` = %s, `pass` = %s WHERE id = %s", (name, email, password, session['sid']))
        con.commit()
        con.close()
        return redirect(url_for("profile"))

    except Exception as e:
        print(f"An error occurred: {e}")
        con.close()
        return "An error occurred"

@app.route("/forgetPassword")
def forgetpassword():
     return render_template("website/Forget_password.html")

@app.route("/forgetpasseworded", methods=["POST"])
def updatepassword():
  

    con = getDb()
    cursor = con.cursor()

    try:
       
        email = request.form["email"]
        password = request.form["pass"]

        cursor.execute("UPDATE `users` SET  `pass` = %s WHERE email = %s", (  password, email))
        con.commit()
        con.close()
        return redirect(url_for("hello_world"))

    except Exception as e:
        print(f"An error occurred: {e}")
        con.close()
        return "An error occurred"


# ------------------------------------------ Admin__Dashboard ------------------------------------

@app.route("/dashboard")
def Dashboard():
    if 'adminSession' not in session:
         return redirect(url_for('login'))   
    con = getDb()
    cursor=con.cursor(dictionary=True)
    
    cursor.execute("select * from users where id = %s ",(session['adminSession'],))
    user = cursor.fetchone()
    cursor.execute("select * from users where is_admin = %s ",(1,))
    admin = cursor.fetchall()
    cursor.execute("select * from users where is_admin = %s ",(0,))
    web_user = cursor.fetchall()
    cursor.execute("SELECT * FROM `services`")
    service = cursor.fetchall()
    cursor.execute("SELECT * FROM `appointment`")
    app= cursor.fetchall()
    cursor.execute("SELECT * FROM `contact`")
    cont= cursor.fetchall()
    con.close()
    return render_template("admin/Dashboard.html", user = user,service=service,admin=admin,web_user=web_user,app=app,cont=cont)

@app.route("/appoint")
def AdminAppointment():
    if 'adminSession' not in session:
         return redirect(url_for('login'))  
    
    con = getDb()
    cursor = con.cursor(dictionary=True)
    
    # Retrieve all appointments with service name
    cursor.execute("""
        SELECT a.*, s_name as service_name
        FROM `appointment` a
        JOIN `services` s ON a.service_id = s.id
    """)
    appointments = cursor.fetchall()
    cursor.execute("select * from users where id = %s ",(session['adminSession'],))
    user = cursor.fetchone()
    con.close()
    return render_template("admin/apointment.html", appointments=appointments,user=user)

@app.route("/appointDel/<int:id>")
def app_del(id):
    if 'adminSession' not in session:
         return redirect(url_for('login'))    
    con = getDb()
    cursor = con.cursor()
    cursor.execute("delete  from appointment where id = %s",(id,))
    con.commit()
    con.close()
    return redirect(url_for('AdminAppointment')) 

@app.route("/admin/profile")
def profileAdmin():
          if 'adminSession' not in session:
              return redirect(url_for('login'))
          
          con = getDb()
          cursor=con.cursor(dictionary=True)
        

          cursor.execute("SELECT * FROM `users` where id = %s",(session['adminSession'],))
          # cursor.execute("SELECT * FROM `users` where id = %s ",(['sid'],))
         
          user = cursor.fetchone()

          con.close()
          return render_template("admin/profile.html",user=user)

@app.route("/adminUpdate", methods=["POST"])
def udateAdminProfile():
    if 'adminSession' not in session:
        return redirect(url_for('login'))

    con = getDb()
    cursor = con.cursor()

    try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]

        cursor.execute("UPDATE `users` SET `name` = %s, `email` = %s, `pass` = %s WHERE id = %s", (name, email, password, session['adminSession']))
        con.commit()
        con.close()
        return redirect(url_for("profileAdmin"))

    except Exception as e:
        print(f"An error occurred: {e}")
        con.close()
        return "An error occurred"

# sevice Crud
@app.route("/service_details")
def services():
    if 'adminSession' not in session:
         return redirect(url_for('login'))   
    con = getDb()
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `services`")
    service = cursor.fetchall()
    cursor.execute("select * from users where id = %s ",(session['adminSession'],))
    user = cursor.fetchone()
    con.close()
    return render_template("admin/servicedetails.html",service=service,user=user)


@app.route("/serviceInsert",methods=["post"])
def servicesadd():
       name = request.form["serviceName"]
       price = request.form["S_price"]
       des = request.form["S_des"]
       con = getDb()
       cursor=con.cursor()
       cursor.execute("INSERT INTO `services`( `s_name`, `description`, `price`) VALUES (%s,%s,%s)",(name,des,price))
       con.commit()
       con.close()
       return redirect(url_for('services'))
     #   return redirect(url_for('service_details'))

@app.route("/serviceDel/<int:id>")
def s_del(id):
       con = getDb()
       cursor = con.cursor()
       cursor.execute("delete  from services where id = %s",(id,))
       con.commit()
       con.close()

       return redirect(url_for('services'))

@app.route("/serivces_Data/<int:id>")
def servicesdata(id):
    if 'adminSession' not in session:
         return redirect(url_for('login'))    
    con = getDb()
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `services` where id = %s",(id,))
    service = cursor.fetchone()
    cursor.execute("select * from users where id = %s ",(session['adminSession'],))
    user = cursor.fetchone()
    con.close()
    return render_template("admin/serviceEdit.html",service=service,user=user)

@app.route("/serviceUpdate/<int:id>",methods=["post"])
def servicesupdate(id):
       name = request.form["serviceName"]
       price = request.form["S_price"]
       des = request.form["S_des"]
       con = getDb()
       cursor=con.cursor()
       cursor.execute("UPDATE `services` SET `s_name`= %s,`description`= %s,`price`= %s  WHERE id= %s ",(name,des,price,id,))
       con.commit()
       con.close()
       return redirect(url_for('services'))

# for fetch the user details on dashboard
@app.route("/userDetails")
def userDetail():
    if 'adminSession' not in session:
         return redirect(url_for('login'))  
       
    con = getDb()
    cursor = con.cursor(dictionary=True)
    cursor.execute("select * from users where is_admin = %s ",(0,))
    users = cursor.fetchall()
    cursor.execute("select * from users where id = %s ",(session['adminSession'],))
    user = cursor.fetchone()
    con.close()
    return render_template("admin/userDetails.html",users=users,user=user)

# for delete the user
@app.route("/userDel/<int:id>")
def userDel(id):
       con = getDb()
       cursor = con.cursor()
       cursor.execute("delete  from users where id = %s",(id,))
       con.commit()
       con.close()
       
       return redirect(url_for('userDetail'))  


#  for update  status od the user
@app.route("/userstatus/<int:id>")
def userstatus(id):

        con = getDb()
        cursor = con.cursor()
        cursor.execute("SELECT `status` FROM `users` WHERE id = %s", (id,))
        user_status = cursor.fetchone()
        if user_status:
            new_status = 1 if user_status[0] == 0 else 0
            cursor.execute("UPDATE `users` SET `status` = %s WHERE id = %s", (new_status, id,))
            con.commit()
        return redirect(url_for('userDetail'))
@app.route("/admin/contact")
def contactDetail():
    if 'adminSession' not in session:
         return redirect(url_for('login'))  
       
    con = getDb()
    cursor = con.cursor(dictionary=True)
    cursor.execute("select * from contact")
    contact = cursor.fetchall()
    cursor.execute("select * from users where id = %s ",(session['adminSession'],))
    user = cursor.fetchone()
    con.close()
    return render_template("admin/contact.html",contact=contact,user=user)
@app.route("/conDel/<int:id>")
def con(id):
       con = getDb()
       cursor = con.cursor()
       cursor.execute("delete  from contact where id = %s",(id,))
       con.commit()
       con.close()
       return redirect(url_for('contactDetail'))  

@app.route("/updateAppointStatus/<int:id>",methods=["post"])
def appStatus(id):

        con = getDb()
        cursor = con.cursor()
        status = request.form["status"]  
        cursor.execute("UPDATE `appointment` SET `status` = %s WHERE id = %s", (status, id,))
        con.commit()
        return redirect(url_for('AdminAppointment'))


if __name__=='__main__':
    app.run(debug=True)