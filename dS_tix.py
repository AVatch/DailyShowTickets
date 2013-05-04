'''
	@AUTHOR: Adrian K Vatchinsky
		 @AVatchinsky
		 akv224@nyu.edu
	Note: Feel free to make this more robust, just let me know ;)

	DESCRIPTION:
		Checks the Daily Show (or Colbert Report) websites every delT
		seconds to see whether or not there are availible tickets.
			If Availible tix	 - pop up browser to let user 
			fill out form
			If No Availible tix	 - try again after delT (s)

		NOTE: This is just me being lazy and wanting to get tickets
		      therefore, there is no error handling or any other 
		      fancy things implemented. I will make this better 
		      if I have the time/interest to continue
'''
import urllib2
import time
import webbrowser
from HTMLParser	 import HTMLParser

#Declare some global variables
site	 = "http://www.thedailyshow.com/tickets"
found	 = False	#keep running until True - aka found tix
key	 = "You're one click away"

#create a subclass and override the handler methods
class MyHTMLParser_Main(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.the_iframe  = ""	#contains iframe link to check for tix
	def handle_starttag(self, tag, attrs):
		if(tag == "iframe"):
			for i in range(len(attrs)):
				if(attrs[i][0]=='id' and attrs[i][1]=='the_iframe'):
					self.the_iframe = attrs[i+1][1]
					break
class MyHTMLParser_Check(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.Data = []
	def handle_data(self,data):
		self.Data.append(data)	

#instantiate the parser
parser1		= MyHTMLParser_Main()
parser2		= MyHTMLParser_Check()

#Get HTML contents of MAIN site
f1 		= urllib2.urlopen(site)
content1 	= f1.read()
parser1.feed(content1)
#Found ticket iframe src, now open it
f2 		= urllib2.urlopen(parser1.the_iframe)
parser1.close()
#loop until found
while(not found):
	content2 	= f2.read() 
	parser2.feed(content2)
	for i in parser2.Data[20:50]:
		if key in i:
			print "Found TIX: opening browser"
			webbrowser.open_new(site)
			found = True
	time.sleep(60)	#check in a minute again
parser2.close()

