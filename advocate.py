
from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from database import *
import uuid
import base64
from AESCLASS import *
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

advocate=Blueprint('advocate',__name__)

@advocate.route("/advocate_home")
def advocate_home():
	if not session.get("lid") is None:

		return render_template("advocate_home.html")
	else:
		return redirect(url_for("public.login"))


@advocate.route("/advocate_view_case_types")
def advocate_view_case_types():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `case_types`"
		data['case']=select(q)

		return render_template("advocate_view_case_types.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route("/advocate_view_law_details")
def advocate_view_law_details():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `law_details`"
		data['law']=select(q)

		return render_template("advocate_view_law_details.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route("/advocate_view_user_cases")
def advocate_view_user_cases():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `cases` INNER JOIN `client` USING(`client_id`) INNER JOIN `case_types` USING(`type_id`)"
		data['cases']=select(q)

		return render_template("advocate_view_user_cases.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route("/adv_view_client_details")
def adv_view_client_details():
	if not session.get("lid") is None:
		data={}
		cid=request.args['cid']
		q="SELECT * FROM `client` WHERE `client_id`='%s'"%(cid)
		data['client']=select(q)

		return render_template("adv_view_client_details.html",data=data)
	else:
		return redirect(url_for("public.login"))

@advocate.route("/adv_send_proposal",methods=['get','post'])
def adv_send_proposal():
	if not session.get("lid") is None:
		data={}
		case_id=request.args['case_id']

		q="SELECT * FROM `proposals` INNER JOIN `cases` USING(`case_id`) where case_id='%s'"%(case_id)
		data['prop']=select(q)

		if 'submit' in request.form:
			fee=request.form['fee']
			q="INSERT INTO `proposals`(`case_id`,`adv_id`,`fee`,`date_time`,`status`) VALUES('%s','%s','%s',now(),'%s')"%(case_id,session['aid'],fee,'pending')
			insert(q)
			flash('proposal has been sent...')
			return redirect(url_for('advocate.advocate_view_user_cases'))

		return render_template("adv_send_proposal.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route("/adv_view_client_assigned_cases",methods=['get','post'])
def adv_view_client_assigned_cases():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,client_assigns.status as a_status FROM `client_assigns` INNER JOIN `client` USING(`client_id`) INNER JOIN `cases` USING(`case_id`) WHERE `adv_id`='%s'"%(session['aid'])
		data['assign']=select(q)

		if 'action' in request.args:
			action=request.args['action']
			aid=request.args['aid']
		else:
			action=None
		if action=='accept':
			q="UPDATE `client_assigns` SET `status`='accepted' WHERE `assign_id`='%s'"%(aid)
			update(q)
			
			flash('Accepted...')
			return redirect(url_for('advocate.adv_view_client_assigned_cases'))
		if action=='reject':
			q="UPDATE `client_assigns` SET `status`='rejected' WHERE `assign_id`='%s'"%(aid)
			update(q)
			flash('Rejected...')
			return redirect(url_for('advocate.adv_view_client_assigned_cases'))



		return render_template("adv_view_client_assigned_cases.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route("/advocate_view_rating")
def advocate_view_rating():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `ratings` INNER JOIN `client` USING(`client_id`) INNER JOIN `advocates` USING(`adv_id`)"
		data['rating']=select(q)

		return render_template("advocate_view_rating.html",data=data)
	else:
		return redirect(url_for("public.login"))

# @advocate.route('adv_view_clients')
# def adv_view_clients():
# 	return render_template('adv_view_clients.html')




@advocate.route("/adv_chat_with_customer",methods=['get','post'])
def adv_chat_with_customer():
	if not session.get("lid") is None:
		data={}
		lid=session['lid']
		cid=request.args['cid']
		aid=session['aid']
		q="SELECT * FROM `chat` WHERE (`sender_id`='%s' AND `receiver_id`='%s' AND `sender_type`='advocate') OR (`sender_id`='%s' AND `receiver_id`='%s' AND `sender_type`='client')"%(lid,cid,cid,lid)
		data['chat']=select(q)
	
		if 'submit' in request.form:
			message=request.form['message']
			q="INSERT INTO `chat`(`sender_id`,sender_type,`receiver_id`,receiver_type,`message`,`date_time`)VALUES('%s','advocate','%s','client','%s',NOW())"%(lid,cid,message)
			insert(q)
			return redirect(url_for('advocate.adv_chat_with_customer',cid=cid))

		return render_template("adv_chat_with_customer.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route("/adv_view_client_cases")
def adv_view_client_cases():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,`proposals`.`status` AS p_status FROM `cases` INNER JOIN `proposals` USING(`case_id`) INNER JOIN `client` USING(`client_id`) INNER JOIN `case_types` USING(`type_id`)  WHERE `adv_id`='%s'"%(session['aid'])
		data['cases']=select(q)

		return render_template("adv_view_client_cases.html",data=data)
	else:
		return redirect(url_for("public.login"))


@advocate.route('/adv_add_case_notes',methods=['get','post'])
def adv_add_case_notes():
	case_id=request.args['case_id']
	data={}
	q="SELECT * FROM `case_notes` inner join cases using(case_id) WHERE `case_id`='%s'"%(case_id)
	data['notes']=select(q)
	if 'submit' in request.form:
		note=request.form['note']
		q="INSERT INTO `case_notes`(`case_id`,`date_time`,`description`) VALUES('%s',NOW(),'%s')"%(case_id,note)
		insert(q)
		flash('Case Note Added...')
		return redirect(url_for('advocate.adv_add_case_notes',case_id=case_id))
	return render_template('adv_add_case_notes.html',data=data)




@advocate.route('/adv_upload_case_files',methods=['get','post'])
def adv_upload_case_files():
	case_id=request.args['case_id']
	data={}
	q="SELECT * FROM `case_files` INNER JOIN cases USING(case_id) WHERE `case_id`='%s'"%(case_id)
	data['upload']=select(q)
	if 'submit' in request.form:
		title=request.form['title']
		file=request.files['file']
		fname = secure_filename(file.filename)
		file.save('static/files/'+fname)
		f = open("static/files/" + fname, "rb")
		a="select * from cases inner join client using(client_id) where case_id='%s'"%(case_id)
		er=select(a)
		client_email=er[0]['email']

		fileread = f.read()
		import random
		v=random.randint(1000,9999)
		key=str(v) 
		print(v)
		print(type(v))
		path=r"D:\Legal Advisor\static\files\\"+fname
		pth=r"D:\Legal Advisor\static\encrypted\\"+fname
		with open(path, "rb") as imageFile:
			stri = base64.b64encode(imageFile.read()).decode('utf-8')
			enc1 = encrypt(stri,key ).decode('utf-8')
			fh = open(pth, "wb")
			fh.write(base64.b64decode(enc1))
			fh.close()
		q="INSERT INTO `case_files`(`file_title`,`case_id`,`key`,`file_name`) VALUES('%s','%s','%s','%s')"%(title,case_id,str(key),fname)
		insert(q)
		msg=str(key)
		try:
			gmail = smtplib.SMTP('smtp.gmail.com', 587)
			gmail.ehlo()
			gmail.starttls()
			gmail.login('projectsriss2020@gmail.com','vroiyiwujcvnvade')
		except Exception as e:
			print("Couldn't setup email!!"+str(e))

		msg = MIMEText(msg)

		msg['Subject'] = 'Encrypted Key Do not Share '

		msg['To'] = client_email

		msg['From'] = 'projectsriss2020@gmail.com'

		try:

			gmail.send_message(msg)
			print(msg)
			flash("EMAIL SENED SUCCESFULLY")
			return redirect(url_for('advocate.adv_upload_case_files',case_id=case_id))


		except Exception as e:
			print("COULDN'T SEND EMAIL", str(e))
			
			return redirect(url_for('advocate.adv_upload_case_files',case_id=case_id))


		

	
	return render_template('adv_upload_case_files.html',data=data)


@advocate.route('/adv_view_meeting_list',methods=['get','post'])
def adv_view_meeting_list():
	data={}
	q="select *,meeting.status as meetstatus from meeting inner join client using(client_id) inner join cases on client.client_id=cases.client_id where adv_id='%s'"%(session['aid'])
	data['meet']=select(q)
	
	if 'action' in request.args:
			action=request.args['action']
			mid=request.args['mid']
	else:
			action=None
	if action=='accept':
			q="UPDATE `meeting` SET `status`='accepted' WHERE `meeting_id`='%s'"%(mid)
			update(q)
			
			flash('Accepted...')
			return redirect(url_for('advocate.adv_view_meeting_list'))
	if action=='reject':
			q="UPDATE `meeting` SET `status`='rejected' WHERE `meeting_id`='%s'"%(mid)
			update(q)
			flash('Rejected...')
			return redirect(url_for('advocate.adv_view_meeting_list'))
	
	if action=='today':
			q="select *,meeting.status as meetstatus from meeting inner join client using(client_id) inner join cases on client.client_id=cases.client_id where adv_id='%s' and date(date)=curdate()"%(session['aid'])
			print(q)
			data['meet']=select(q)



	
	return render_template('adv_view_meeting_list.html',data=data)

@advocate.route("/advocate_view_hearing_chat",methods=['get','post'])
def advocate_view_hearing_chat():
	if not session.get("lid") is None:
		data={}
		id=request.args['case_id']
		q="SELECT * FROM hearing INNER JOIN cases USING (case_id) INNER JOIN clerk USING (clerk_id) WHERE case_id='%s'"%(id)
		data['view']=select(q)
		return render_template("advocate_view_hearing_chat.html",data=data)
	else:
		return redirect(url_for("public.login"))




		