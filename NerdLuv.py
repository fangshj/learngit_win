 #coding=utf-8
'''
SYSU school of software
13331048  fangshaojie
web2.0  stage2 homework4:this homework is about to make a page with get and post method
*I add the new function of uploading photo*
'''
import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import re
import os

from tornado.options import define, options
define("ports", default=8888, help="Run on the given port ", type=int)

#create a class to store the infomation of a user
class user(object):
	def __init__(self, img_url, name, gender, age, type, OS, rating):
		self.img_url = img_url
		self.name = name
		self.gender = gender
		self.age = age
		self.type = type
		self.OS = OS
		self.rating = rating

 #deal with the get request
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render( 'index.html' )

class ResultsHandler(tornado.web.RequestHandler):
#deal with the post request
	def post(self): 
 #get the argumetnt 
		name = self.get_argument("name", None)
		gender = self.get_argument("gender", None)
		age = self.get_argument("age", None)
		type = self.get_argument("type", None)
		OS = self.get_argument("OS", None)
		seekMale = self.get_argument("seekMale", None)
		seekFemale = self.get_argument("seekFemale", None)
		minAge = self.get_argument("minAge", None)
		maxAge = self.get_argument("maxAge", None)

#deal with img uploaded
		upload_path=os.path.join(os.path.dirname(__file__),'files')  #文件的暂存路径
		file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
		for meta in file_metas:
			new_path_filename =  r'static/images/' + name.lower().replace(' ', '_') + '.jpg'
			with open(new_path_filename,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
				up.write(meta['body'])

#read all the information in the singles.txt
		output = open('static/singles.txt', 'r')
		outputList = output.readlines()
		output.close()

		matchList=[]
		for one in outputList:
			newone = one.split(',')
			tempname = newone[0].lower()
			tempname = tempname.replace(' ', '_')

			filename = './static/images/' + tempname + '.jpg' #check if the picture of the user exists
			if os.path.exists(filename):
				iima_url = '../static/images/' + tempname + '.jpg'
			else:
				iima_url = "../static/images/default_user.jpg"

			iname = newone[0]
			igender = newone[1]
			iage = newone[2]
			itype = newone[3]
			iOS = newone[4]
			irating = 0
#match the gender of each other
			if seekMale:
				if igender != 'M':
					if not seekFemale:
						continue
			else:
				if igender != 'F':
					continue
			if not re.match(gender, newone[5]):
				continue
#match the rating points
			if iage >= minAge and iage <= maxAge:# match age
				if age >= newone[6] and age <= newone[7]:
					irating += 1

			if OS == iOS and OS != 'other':# match OS
				irating += 2

			if type[0] == itype[0]:# match personality type
				irating += 1
			if type[1] == itype[1]:
				irating += 1
			if type[2] == itype[2]:
				irating += 1
			if type[3] == itype[3]:
				irating += 1
#check if the rating point if meet the standard of at least 3
			if irating >= 3:
				iuser = user(iima_url, iname, igender, iage, itype, iOS, irating)
				matchList.append(iuser)
#write the information of the new user into singles.txt
		if seekFemale and seekMale: #turn the gender the new user want into 'M' or 'F' or 'MF'
			seek = 'MF'
		elif seekMale:
			seek = 'M'
		else:
			seek = 'F'
		intput = open('static/singles.txt', 'a')  #write the information into the suckers.txt
		intput.write(name+','+gender+','+age+','+type+','+OS+','+seek+','+minAge+','+maxAge+'\n')
		intput.close()

		self.render('results.html', matchList = matchList)



if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r"/", MainHandler), (r"/results.html", ResultsHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "template"),
		static_path=os.path.join(os.path.dirname(__file__), "static"),
		debug=True
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.ports)
	tornado.ioloop.IOLoop.instance().start()