import urllib2, urllib, sys, re, os, unicodedata, time, json
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

  
###################################################################################################################
#
#   Generally a success, extracted html is javascript supported now! Great success.
#   But, the program is unable to gracefully shutdown. It hangs and does nothing except eating up memory and processing power
#
###################################################################################################################
#
# Some troubleshooting methods:
# - add in signals like loadStarted, loadProgress to indicate a load has been started and is in progress for troubleshooting purposes.
# 
# A progress bar has sort of been created from createrequest as i have noticed that that function had been ran multiple times and it corresponds with the load progress.
###########################################################################################################################################################


# Things to note
#	
# myURL+course_id+end_part_url ==> complete url
myURL = "https://ntulearn.ntu.edu.sg/webapps/ntu-hdlcoursephoto-BBLEARN/links/index.jsp?course_id=_"
end_part_url = "_1"
course_id = start_course_id #counter
start_course_id = 10000
end_course_id = 90000


def writeToFile(data, filename, mode):
	f = open(filename, mode)
	f.write(data)
	f.close()
 
def banner(text, ch='=', length=78):
	spaced_text = ' %s ' % text
	banner = ''+spaced_text.center(length, ch)+''
	return banner
 
def maketiny(url):# make tinyurl from long url, #useless
	try:
		#print "http://tinyurl.com/api-create.php?url=" + urllib.quote_plus(url)
		html = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + urllib.quote_plus(url))
		tiny = str(html.read())
		return tiny
	except Exception, e:
		print str(e)
		return False	
		
def makegoo(url): #useless
	post_url = 'https://www.googleapis.com/urlshortener/v1/url'
	postdata = {'longUrl':url}
	headers = {'Content-Type':'application/json'}
	req = urllib2.Request(
		post_url,
		json.dumps(postdata),
		headers
		)
	ret = urllib2.urlopen(req).read()
	print ret
	return json.loads(ret)['id']
	
def doIt(html):
	line = html
	try:
		print '[+] Getting urls...'
		# if its an error page
		# return true

		# if its not then return false
		return false
	except:
		print 'gg'
		quit()
 
class MyNetworkAccessManager(QNetworkAccessManager):
	def __init__(self, url):
		QNetworkAccessManager.__init__(self)
		self.request = QNetworkRequest(QUrl(url))
		self.reply = self.get(self.request)
		
	def createRequest(self, operation, request, data):
		#request.setRawHeader("Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7");
		#print 'createRequest: url is '+request.url()
		#print 'mymanager handles ',request.url()
		#file = open('request.html', 'a')
		#file.write(request.url().toString()+'\n======================================================================\n\n\n\n\n\n\n')
		#file.close()
		request.setRawHeader("Connection","keep-alive");
		request.setRawHeader("Host", "google.com")
		request.setRawHeader("Proxy-Connection", "keep-alive")
		request.setRawHeader("Cache-Control", "max-age=0")
		request.setRawHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
		request.setRawHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36")
		request.setRawHeader("DNT", "1")
		request.setRawHeader("Referer", "http://www.google.com")
		request.setRawHeader("Accept-Encoding", "deflate, sdch")
		request.setRawHeader("Accept-Language", "en-US,en;q=0.8")
		request.setRawHeader("Cookie", "")
		#a = request.rawHeader("Cookie")
		#print a
		sys.stdout.write('.') # progress bar
		return QNetworkAccessManager.createRequest( self, operation, request, data )
		
		
class Crawler( QWebPage ):
	def __init__(self, url):# Reminder to add more signals, loadStarted, loadProgress if needed
		QWebPage.__init__( self )
		self._url = url
		manager = MyNetworkAccessManager(url)
		self.setNetworkAccessManager(manager)
		self.loadFinished.connect(self._loadFinished)
		self.mainFrame().load( QUrl( self._url ) )
	
	def _loadFinished( self, result ):
		global course_id
		global myURL
		global end_part_url
		global end_course_id
		print 'LOAD FINISHED'
		self.frame = self.mainFrame()
		html = str(self.mainFrame().toHtml().replace("&amp;", "&").toUtf8()).decode("utf-8") #make to something, doesn't really work
		html = html.encode('ascii', 'ignore') # change to ascii, and ignore those that cannot be converted.
		
		# Do a check if its an error page
		# if its an error, skip it
		# else write html to file
		if(!doIt(html)):#this will regex and check if its an error page
			# if true, its an error page, so skip it
			# if false, its an ok page, so write to file
			# Write html to file
			writeToFile(html, course_id+'.html', 'wb')
		
		course_id += 1
		
		#OVER HERE LOAD NEXT URL
		if(course_id<=end_course_id):#continue or not
			print 'start loading '+str(course_id)
			self.mainFrame().load( QUrl(myURL + str(course_id) + end_part_url)
		else:
			print '\n\n'+banner('COMPLETED')
			print banner('BY TEMPUSER   CAA260116')+'\n\n'
			app.quit()
			sys.exit(0)
#main
print '\n\n\n'+banner('WELCOME TO NTU STALKER')+'\n\n'
print banner('BY TEMPUSER   CAA260116')+'\n\n\n'
url = myURL + str(start_course_id) + end_part_url
print url #could be removed
app = QApplication(sys.argv)
crawler = Crawler(url)
sys.exit(app.exec_())
print 'quitting'
sys.exit(0)
# still cannot gracefully close program, might be a problem if we are going to implement it with the auto downloader
