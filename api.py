from flask import *
from database import *
import demjson
import base64
from AESCLASS import *
from werkzeug.utils import secure_filename


api = Blueprint('api',__name__)


@api.route('/login',methods=['get','post'])
def login():
	data={}
	username = request.args['username']
	password = request.args['password']
	q = "select * from login where username='%s' and password='%s'" % (username,password)
	res = select(q)
	if res:
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	return  demjson.encode(data)

@api.route('/register',methods=['get','post'])
def register():
	data={}
	fname = request.args['fname']
	lname = request.args['lname']
	gender = request.args['gender']
	dob = request.args['dob']
	phone = request.args['phone']
	email = request.args['email']
	hname = request.args['hname']
	place=request.args['place']
	pin = request.args['pin']
	uname=request.args['uname']
	passw=request.args['passw']

	q1="INSERT INTO `login`(`username`,`password`,`usertype`)VALUES('%s','%s','user_pending')"%(uname,passw)
	id=insert(q1)
	q="INSERT INTO `client`(`login_id`,`first_name`,`last_name`,`gender`,`dob`,`phone`,`email`,`house_name`,`place`,`pincode`)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id,fname,lname,gender,dob,phone,email,hname,place,pin)
	c=insert(q)
	if(c>0):
		data['status']  = 'success'
	else:
		data['status']	= 'failed'
		data['method']  ='register'
	return demjson.encode(data)


@api.route('/viewlawdetails',methods=['get','post'])
def viewlawdetails():
	data={}

	q="SELECT * FROM `law_details`"
	res=select(q)
	print(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewlawdetails'
	return  demjson.encode(data)

@api.route('/viewcasetype',methods=['get','post'])
def viewcasetype():
	data={}

	q="SELECT * FROM `case_types`"
	res=select(q)
	print(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewcasetype'
	return  demjson.encode(data)

@api.route('/managecase',methods=['get','post'])
def managecase():
	data={}
	login_id=request.args['login_id']
	title = request.args['title']
	desc = request.args['desc']
	cdate = request.args['cdate']
	stn = request.args['stn']
	pin = request.args['pin']
	phone = request.args['phone']
	type_ids = request.args['type_ids']
	
	q="INSERT INTO `cases`(`client_id`,`type_id`,`title`,`description`,`case_date`,`police_station`,`pincode`,`phone`,`status`)VALUES((select client_id from client where login_id='%s'),'%s','%s','%s','%s','%s','%s','%s','pending')"%(login_id,type_ids,title,desc,cdate,stn,pin,phone)
	c=insert(q)

	if(c>0):
		data['status']  = 'success'
	else:
		data['status']	= 'failed'
	data['method']  ='managecase'
	return demjson.encode(data)


@api.route('/viewcases',methods=['get','post'])
def viewcases():
	data={}

	login_id=request.args['login_id']

	q="SELECT * FROM `cases` inner join case_types using(type_id) WHERE `client_id`=(select client_id from client where login_id='%s')"%(login_id)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewcases'
	return  demjson.encode(data)


@api.route('/viewproposals',methods=['get','post'])
def viewproposals():
	data={}
	cid=request.args['case_id']

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS adv_name,proposals.status as pstatus FROM `proposals` INNER JOIN `cases` USING(`case_id`) INNER JOIN `advocates` USING(`adv_id`) where case_id='%s'"%(cid)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewproposals'
	return  demjson.encode(data)

@api.route('/viewadvocates',methods=['get','post'])
def viewadvocates():
	data={}
	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS adv_name FROM `advocates`"
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewadvocates'
	return  demjson.encode(data)

@api.route('/assigncase',methods=['get','post'])
def assigncase():
	data={}

	login_id=request.args['login_id']

	q="SELECT * FROM `cases` inner join case_types using(type_id) WHERE `client_id`=(select client_id from client where login_id='%s') AND `status`='pending'"%(login_id)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'assigncase'
	return  demjson.encode(data)

@api.route('/viewongoingcases',methods=['get','post'])
def viewongoingcases():
	data={}
	login_id=request.args['login_id']

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS adv_name FROM `client_assigns` INNER JOIN `cases` USING(`case_id`) INNER JOIN `advocates` USING(`adv_id`) INNER JOIN`case_types` USING(`type_id`) WHERE `client_assigns`.`client_id`=(SELECT client_id FROM `client` WHERE login_id='%s') AND `client_assigns`.`status`='accepted'"%(login_id)
	print(q)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewongoingcases'
	return  demjson.encode(data)

@api.route('/viewadvocatedetails',methods=['get','post'])
def viewadvocatedetails():
	data={}

	aid=request.args['adv_id']

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS advocate_name FROM `advocates` WHERE `adv_id`='%s'"%(aid)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewadvocatedetails'
	return  demjson.encode(data)

@api.route('/viewcasenotes',methods=['get','post'])
def viewcasenotes():
	data={}

	cid=request.args['case_id']

	q="SELECT * FROM `case_notes` INNER JOIN `cases` USING(`case_id`) WHERE `case_id`='%s'"%(cid)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewcasenotes'
	return  demjson.encode(data)


@api.route('/viewcasefiles',methods=['get','post'])
def viewcasefiles():
	data={}

	# cid=request.args['case_id']

	# q="SELECT * FROM `case_files` INNER JOIN `cases` USING(`case_id`) WHERE `case_id`='%s'"%(cid)
	# res=select(q)
	# filename=res[0]['file_name']
	key=request.args['key']
	a="select * from case_files w"
	password="#34^%%$w5454"
	pth1=r"C:\RISS PROJECTS D\FISAT\Legal Advisor\static\encrypted\\"+filename
	pth2=r"C:\RISS PROJECTS D\FISAT\Legal Advisor\static\downloads\\"+filename
	print(pth1)
	print(pth2)
	with open(pth1, "rb") as imageFile:
		stri = base64.b64encode(imageFile.read()).decode('utf-8')
		dec2 = decrypt(stri, key).decode('utf-8')
		fh1 = open(pth2, "wb")
		fh1.write(base64.b64decode(dec2))
		fh1.close()
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewcasefiles'
	return  demjson.encode(data)

# @api.route('/viewcasefiles',methods=['get','post'])
# def viewcasefiles():
# 	data={}

# 	cid=requet.args['case_id']

# 	q="SELECT * FROM `case_files` WHERE `case_id`='%s'"%(cid)
# 	res=select(q)
# 	if res:
# 		data['status']  = 'success'
		
# 		data['data'] = res
# 	else:
# 		data['status']	= 'failed'
# 	data['method']  = 'viewcasefiles'
# 	return  demjson.encode(data)

@api.route('/complaint',methods=['get','post'])
def complaint():
	data={}
	login_id=request.args['login_id']
	desc = request.args['desc']

	q="INSERT INTO `complaints`(`client_id`,`desc`,`reply`,`date_time`) VALUES((select client_id from client where login_id='%s'),'%s','pending',NOW())"%(login_id,desc)
	res=insert(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'complaint'
	return  demjson.encode(data)

@api.route('/viewcomplaints',methods=['get','post'])
def viewcomplaints():
	data={}

	login_id=request.args['login_id']

	q="SELECT * FROM `complaints` WHERE `client_id`=(select client_id from client where login_id='%s')"%(login_id)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'viewcomplaints'
	return  demjson.encode(data)

@api.route('/accept_proposal',methods=['get','post'])
def accept_proposal():
	data={}
	pid=request.args['pids']
	cid=request.args['cid']
	lid=request.args['login_id']
	adid=request.args['advid']
	fee=request.args['fee']
	q="UPDATE `proposals` SET `status`='accepted' WHERE `proposal_id`='%s'"%(pid)
	res=update(q)
	e="insert into client_assigns values(null,(select client_id from client where login_id='%s'),'%s','%s',now(),'assigned')"%(lid,adid,cid)
	res=insert(e)
	r="insert into payment values(null,(select client_id from client where login_id='%s'),'%s','%s',curdate(),'%s')"%(lid,cid,fee,adid)
	res=insert(r)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'accept_proposal'
	return  demjson.encode(data)


@api.route('/reject_proposal',methods=['get','post'])
def reject_proposal():
	data={}

	pid=request.args['pids']

	q="UPDATE `proposals` SET `status`='rejected' WHERE `proposal_id`='%s'"%(pid)
	res=update(q)
	if res:
		data['status']  = 'success'

		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'reject_proposal'
	return  demjson.encode(data)


@api.route('/assigncase_to_adv',methods=['get','post'])
def assigncase_to_adv():
	data={}

	aid=request.args['adv_id']
	cid=request.args['case_id']
	lid=request.args['login_id']

	q="INSERT INTO `client_assigns`(`client_id`,`adv_id`,`case_id`,`date_time`,`status`) VALUES((select client_id from client where login_id='%s'),'%s','%s',NOW(),'assigned')"%(lid,aid,cid)
	insert(q)
	q="UPDATE `cases` SET `status`='assigned' WHERE `case_id`='%s'"%(cid)
	res=update(q)


	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'assigncase_to_adv'
	return  demjson.encode(data)


@api.route('/chat',methods=['get','post'])
def chat():
	data={}

	sid=request.args['sender_id']
	rid=request.args['receiver_id']
	msg=request.args['details']

	q="INSERT INTO `chat`(`sender_id`,`sender_type`,`receiver_id`,`receiver_type`,`message`,`date_time`)VALUES('%s','client','%s','advocate','%s',NOW())"%(sid,rid,msg)
	res=insert(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'chat'
	return  demjson.encode(data)

	
@api.route('/chatdetail',methods=['get','post'])
def chatdetail():
	data={}

	sid=request.args['sender_id']
	rid=request.args['receiver_id']


	q="SELECT * FROM `chat` WHERE (`receiver_id`='%s' AND `sender_id`='%s') or (`receiver_id`='%s' AND `sender_id`='%s')"%(sid,rid,rid,sid)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'chatdetail'
	return  demjson.encode(data)

	

@api.route('/chattedadv',methods=['get','post'])
def chattedadv():
	data={}

	lid=request.args['login_id']

	# q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS advocate_name FROM `chat` INNER JOIN `advocates` ON `advocates`.`logid`=`chat`.`receiver_id` WHERE `sender_id`='%s' GROUP BY receiver_id"%(lid)
	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS advocate_name FROM `chat` INNER JOIN `advocates` ON `advocates`.`logid`=`chat`.`sender_id` WHERE `receiver_id`='%s' GROUP BY receiver_id"%(lid)
	res=select(q)
	if res:
		data['status']  = 'success'
		
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']  = 'chattedadv'
	return  demjson.encode(data)


@api.route('/rate_advocate',methods=['get','post'])
def rate_advocate():

	data={}

	login_id=request.args['login_id']
	adv_id=request.args['adv_id']
	rating=request.args['rating']
	review=request.args['review']

	q="SELECT * FROM `ratings` WHERE `adv_id`='%s' AND `client_id`=(select client_id from client where login_id='%s')"%(adv_id,login_id)
	res=select(q)
	if res:

		q="UPDATE `ratings` SET `rate`='%s',`review`='%s',`date_time`=NOW() WHERE `adv_id`='%s'"%(rating,review,adv_id)
		update(q)
		data['status'] = 'success'
	else:
		q="INSERT INTO `ratings`(`client_id`,`adv_id`,`rate`,`review`,`date_time`)VALUES((select client_id from client where login_id='%s'),'%s','%s','%s',NOW())"%(login_id,adv_id,rating,review)
		id=insert(q)
		if id>0:
			data['status'] = 'success'
			
		else:
			data['status'] = 'failed'
	data['method'] = 'rate_advocate'
	return demjson.encode(data)


@api.route('/view_rating',methods=['get','post'])
def view_rating():
	data = {}

	login_id=request.args['login_id']
	adv_id=request.args['adv_id']
	
	q=" SELECT * FROM `ratings` WHERE `adv_id`='%s' AND `client_id`=(select client_id from client where login_id='%s')"%(adv_id,login_id)
	print(q)
	result=select(q)
	if result:
		data['status'] = 'success'
		data['data'] = result[0]['rate']
		data['data1'] = result[0]['review']
		
	else:
		data['status'] = 'failed'
	data['method'] = 'view_rating'
	return demjson.encode(data)






@api.route('/meeting',methods=['get','post'])
def meeting():
	data={}
	data['method']  = 'managecase'
	login_id=request.args['lid']
	time=request.args['time']
	date=request.args['date']
	advid=request.args['advid']
	q="insert into meeting values(null,'%s','%s','%s','pending',(select client_id from client where login_id='%s'))"%(advid,time,date,login_id)
	r=insert(q)
	if r:
		data['status'] = 'success'
	else:
		data['status'] = 'failed'
	return str(data)



@api.route('/key',methods=['get','post'])
def key():
	data={}
	data['method']='managecase'
	key=request.args['title']
	logid=request.args['login_id']
	qa="select * from case_files where `key`='%s'"%(key)
	res=select(qa)
	img=res[0]['file_name']
	pth1="static/encrypted/"+img
	pth2=r"static\\downloads\\"+img
	with open(pth1, "rb") as imageFile:
		print(imageFile,'1111111111111111111111111111111111111111111111111111')
		stri = base64.b64encode(imageFile.read()).decode('utf-8')
		dec2 = decrypt(stri, key).decode('utf-8')
		fh1 = open(pth2, "wb")
		vak=fh1.write(base64.b64decode(dec2))
		data['path']='static\downloads\\'+img

		print('static\downloads\\'+img,',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
		data['status']='success'
		return str(data)
