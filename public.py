from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from database import*
import uuid

public=Blueprint("public",__name__)

@public.route("/")
def home():
	session.clear()
	return render_template("home.html")

@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'submit' in request.form:
		uname=request.form['uname']
		passs=request.form['passs']
		q="select * from login where username='%s' and password='%s'" %(uname,passs)
		res=select(q)
		if res:
			session['lid']=res[0]['logid']
			if res[0]['usertype']=="admin":
				flash("Logging in")			
				return redirect(url_for("admin.admin_home"))

			elif res[0]['usertype']=="advocate":
				q="select * from advocates where logid='%s'"%(res[0]['logid'])
				res1=select(q)
				if res1:
					session['aid']=res1[0]['adv_id']
					flash("Logging in")
					return redirect(url_for("advocate.advocate_home"))
			elif res[0]['usertype']=="clerk":
				q="select * from clerk where logid='%s'"%(res[0]['logid'])
				res1=select(q)
				if res1:
					session['clerk']=res1[0]['clerk_id']
					flash("Logging in")
					return redirect(url_for("clerk.clerk_home"))
			else:
				flash("Registration Under Process")
		flash("You are Not Registered")
	return render_template("login.html")



@public.route('/advocate_register',methods=['get','post'])
def advocate_register():
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		hname=request.form['hname']
		place=request.form['place']
		qual=request.form['qual']
		gender=request.form['gender']
		phone=request.form['phone']
		email=request.form['email']
		file=request.files['file']
		path='static/adv/'+str(uuid.uuid4())+file.filename
		file.save(path)
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('%s','%s','adv_pending')"%(uname,pwd)
		logid=insert(q)
		q="INSERT INTO `advocates`(`logid`,`first_name`,`last_name`,`qualification`,`gender`,`phone`,`email`,`house_name`,`place`,`image`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(logid,fname,lname,qual,gender,phone,email,hname,place,path)
		insert(q)
		flash('Registered Successfully...')
		return redirect(url_for('public.login'))
	return render_template('advocate_register.html')	