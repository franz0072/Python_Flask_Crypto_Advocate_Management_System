from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from database import*

admin=Blueprint('admin',__name__)

@admin.route("/admin_home")
def admin_home():
	if not session.get("lid") is None:
		return render_template("admin_home.html")
	else:
		return redirect(url_for("public.login"))


@admin.route("/admin_view_advocate",methods=['get','post'])
def admin_view_advocate():
	if not session.get("lid") is None:
		data={}
		q="select *,concat(first_name,' ',last_name) as fullname from advocates inner join login using(logid)"
		data['view']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='accept':
			q="update login set usertype='advocate' where logid='%s'"%(id)
			update(q)
			flash("Accepted")
			return redirect(url_for("admin.admin_view_advocate"))
		if action=='reject':
			q="update login set usertype='rejected' where logid='%s'"%(id)
			update(q)
			flash("Rejected")
			return redirect(url_for("admin.admin_view_advocate"))
		return render_template("admin_view_advocate.html",data=data)
	else:
		return redirect(url_for("public.login"))
	


@admin.route("/admin_view_users",methods=['get','post'])
def admin_view_users():
	if not session.get("lid") is None:
		data={}
		q="select *,concat(first_name,' ',last_name) as fullname from client inner join login on client.login_id=login.logid where usertype='user_pending'"
		data['view']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='accept':
			q="update login set usertype='user' where logid='%s'"%(id)
			update(q)
			flash("Accepted")
			return redirect(url_for("admin.admin_view_users"))
		if action=='reject':
			q="update login set usertype='rejected' where logid='%s'"%(id)
			update(q)
			flash("Rejected")
			return redirect(url_for("admin.admin_view_users"))
		return render_template("admin_view_users.html",data=data)
	else:
		return redirect(url_for("public.login"))



@admin.route("/admin_manage_clerk",methods=['get','post'])
def admin_manage_clerk():
	if not session.get("lid") is None:
		data={}
		q="select * from clerk"
		data['view']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			sid=request.args['cid']
		else:
			action=None
		if action=='remove':
			q="DELETE FROM clerk WHERE clerk_id='%s'"%(sid)
			delete(q)
			flash("Removed")
			return redirect(url_for("admin.admin_manage_clerk"))
		if action=='update':
			q="select * from clerk where clerk_id='%s'"%(sid)
			res=select(q)
			data['viewupdates']=res
		if 'updatesubmit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			qual=request.form['qual']
			gender=request.form['gender']
			phone=request.form['phone']
			email=request.form['email']
			q="update `clerk` set  `fname`='%s', `lname`='%s', `qualification`='%s', `gender`='%s', `phone`='%s', `email`='%s', `house`='%s', `place`='%s' where clerk_id='%s'"%(fname,lname,qual,gender,phone,email,hname,place,sid)
			update(q)
			flash("Changes Saved")
			return redirect(url_for("admin.admin_manage_clerk"))
		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			hname=request.form['hname']
			place=request.form['place']
			qual=request.form['qual']
			gender=request.form['gender']
			phone=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('%s','%s','clerk')"%(uname,pwd)
			logid=insert(q)
			q="INSERT INTO `clerk`(`logid`,`fname`,`lname`,`qualification`,`gender`,`phone`,`email`,`house`,`place`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(logid,fname,lname,qual,gender,phone,email,hname,place)
			insert(q)
			flash('Registered Successfully...')
			return redirect(url_for('admin.admin_manage_clerk'))
		return render_template("admin_manage_clerk.html",data=data)
	else:
		return redirect(url_for("public.login"))






@admin.route("/admin_manage_law_details",methods=['get','post'])
def admin_manage_law_details():
	if not session.get("lid") is None:
		data={}
		q="select * from law_details"
		data['view']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			sid=request.args['cid']
		else:
			action=None
		if action=='remove':
			q="DELETE FROM law_details WHERE law_id='%s'"%(sid)
			delete(q)
			flash("Removed")
			return redirect(url_for("admin.admin_manage_law_details"))
		if action=='update':
			q="select * from law_details where law_id='%s'"%(sid)
			res=select(q)
			data['viewupdates']=res
		if 'updatesubmit' in request.form:
			title=request.form['crime_type_name']
			ipc_code=request.form['ipc_code']
			penalty=request.form['penalty']
			discription=request.form['discription']
			q="UPDATE law_details set `title`='%s',`ipc_code`='%s',`description`='%s',`penalty`='%s' where law_id='%s'"%(title,ipc_code,discription,penalty,sid)
			update(q)
			flash("Changes Saved")
			return redirect(url_for("admin.admin_manage_law_details"))
		if 'submit' in request.form:
			title=request.form['crime_type_name']
			ipc_code=request.form['ipc_code']
			penalty=request.form['penalty']
			discription=request.form['discription']
			q="INSERT INTO law_details(`title`,`ipc_code`,`description`,`penalty`)VALUES('%s','%s','%s','%s')"%(title,ipc_code,discription,penalty)
			insert(q)
			flash("Added")
			return redirect(url_for("admin.admin_manage_law_details"))
		return render_template("admin_manage_law_details.html",data=data)
	else:
		return redirect(url_for("public.login"))

# admin_manage_law_details
@admin.route("/admin_manage_case_types",methods=['get','post'])
def admin_manage_case_types():
	if not session.get("lid") is None:
		data={}
		q="select * from case_types"
		data['view']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			sid=request.args['cid']
		else:
			action=None
		if action=='remove':
			q="DELETE FROM case_types WHERE type_id='%s'"%(sid)
			delete(q)
			flash("Removed")
			return redirect(url_for("admin.admin_manage_case_types"))
		if action=='update':
			q="select * from case_types where type_id='%s'"%(sid)
			res=select(q)
			data['viewupdates']=res
		if 'updatesubmit' in request.form:
			crime_type_name=request.form['crime_type_name']
			discription=request.form['discription']
			q="update `case_types` set  `type_name`='%s', `description`='%s' where type_id='%s'"%(crime_type_name,discription,sid)
			update(q)
			flash("Changes Saved")
			return redirect(url_for("admin.admin_manage_case_types"))
		if 'submit' in request.form:
			crime_type_name=request.form['crime_type_name']
			discription=request.form['discription']
			q="INSERT INTO `case_types`(`type_name`, `description`) VALUES ('%s','%s')"%(crime_type_name,discription)
			insert(q)
			flash("Added")
			return redirect(url_for("admin.admin_manage_case_types"))
		return render_template("admin_manage_case_types.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route("/admin_view_case_advocates",methods=['get','post'])
def admin_view_case_advocates():
	if not session.get("lid") is None:
		data={}
		id=request.args['id']
		q="SELECT *,CONCAT(advocates.`first_name`,' ',advocates.`last_name`)AS adv_name,CONCAT(client.`first_name`,' ',client.`last_name`)AS c_name FROM proposals INNER JOIN cases USING(case_id) INNER JOIN advocates USING(adv_id) INNER JOIN CLIENT USING(client_id) where client_id='%s'"%(id)
		print(q)
		data['view']=select(q)
		return render_template("admin_view_case_advocates.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route("/admin_view_complaints",methods=['get','post'])
def admin_view_feedback():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(first_name,' ',last_name) AS username FROM complaints INNER JOIN client USING(client_id)"
		data['msgs']=select(q)
		i=1
		for row in data['msgs']:
			if 'submit'+str(i) in request.form:
				reply=request.form['reply'+str(i)]
				q="update complaints set reply='%s',date_time=now() where complaint_id='%s'"%(reply,row['complaint_id'])
				update(q)
				flash("Replied")
				return redirect(url_for("admin.admin_view_feedback"))
			i=i+1
		return render_template("admin_view_feedback.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route("/admin_view_cases",methods=['get','post'])
def admin_view_cases():
	if not session.get("lid") is None:
		data={}
		cid=request.args['id']
		q="SELECT *,CONCAT(first_name,' ',last_name) as fullname,cases.description as des,cases.phone as cp,cases.pincode as cpin,case_types.description as csd FROM cases INNER JOIN case_types USING(type_id) inner join client using(client_id) where client_id='%s'"%(cid)
		print(q)
		data['view']=select(q)
		return render_template("admin_view_cases.html",data=data)
	else:
		return redirect(url_for("public.login"))

@admin.route("/admin_view_registered_users",methods=['get','post'])
def admin_view_registered_users():
	if not session.get("lid") is None:
		data={}
		q="select *,concat(first_name,' ',last_name) as fullname from client"
		data['view']=select(q)
		return render_template("admin_view_registered_users.html",data=data)
	else:
		return redirect(url_for("public.login"))
	


@admin.route("/admin_view_hearing_chat",methods=['get','post'])
def admin_view_hearing_chat():
	if not session.get("lid") is None:
		data={}
		id=request.args['id']
		q="SELECT * FROM hearing INNER JOIN cases USING (case_id) INNER JOIN clerk USING (clerk_id) WHERE case_id='%s'"%(id)
		data['view']=select(q)
		return render_template("admin_view_hearing_chat.html",data=data)
	else:
		return redirect(url_for("public.login"))	


@admin.route("/admin_view_payment",methods=['get','post'])
def admin_view_payment():
	if not session.get("lid") is None:
		data={}
		id=request.args['id']
		q="SELECT * FROM payment INNER JOIN cases USING (case_id) WHERE case_id='%s'"%(id)
		data['view']=select(q)
		return render_template("admin_view_payment.html",data=data)
	else:
		return redirect(url_for("public.login"))
# @admin.route("/admin_view_advocate",methods=['get','post'])
# def admin_view_advocate():
# 	if not session.get("lid") is None:
# 		data={}
# 		q="select *,concat(first_name,' ',last_name) as fullname from advocates inner join login using(logid)"
# 		data['view']=select(q)
# 		if 'action' in request.args:
# 			action=request.args['action']
# 			id=request.args['id']
# 		else:
# 			action=None
# 		if action=='accept':
# 			q="update login set usertype='advocate' where logid='%s'"%(id)
# 			update(q)
# 			flash("Accepted")
# 			return redirect(url_for("admin.admin_view_advocate"))
# 		if action=='reject':
# 			q="update login set usertype='rejected' where logid='%s'"%(id)
# 			update(q)
# 			flash("Rejected")
# 			return redirect(url_for("admin.admin_view_advocate"))
# 		return render_template("admin_view_advocate.html",data=data)
# 	else:
# 		return redirect(url_for("public.login"))