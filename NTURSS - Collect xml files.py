import urllib2, urllib, sys, re, time


def maketiny(url):# make tinyurl from long url
	try:
		html = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url)
		tiny = str(html.read())
		return tiny
	except:
		return False
#if len(sys.argv) < 2:
#    print "Usage: python %s <link>"%sys.argv[0]
#    quit()
def writeToFile(data, filename, mode):
	f = open(filename, mode)
	f.write(data)
	f.close()
	
def requestURL(filenostr):
	input = 'http://presentur.ntu.edu.sg/podcast/rss/rss'+ filenostr +'_2.xml'
	data = urllib2.urlopen(input).read()
	return data

# Range to search for xml (eg. 1000 - 6300), current stop at 5590 (CAA: 061115_0407H)
start = 1000
stop = 6300
fileno = 0
	
for fileno in range(start, stop):	
	try:
		#loop starts here
		filenostr = str(fileno)
		print '\n\n\n[+] Searching for File '+filenostr+'.xml : '
		data = requestURL(filenostr)
		print '[+] Successfully requested URL'
		#<title>15S1-L6115</title>
		#title = re.findall("<a rel=\"nofollow\" target=\"_blank\" 	href=\"(.+?)\">.+?<\/a>",data)
		title = re.findall("<title>(.+?)<\/title>",data)
		print 'Copying file : File '+filenostr+'.xml ==> '+title[0]+''
		tableEntry = 'File '+filenostr+'.xml ==> '+title[0]+'\n'
		writeToFile(tableEntry, '_TableOfContents.txt', 'a')
		writeToFile(data, '.\\Archive\\'+filenostr+'.xml', 'w')
		time.sleep(0.1)
		if(fileno%200 == 0):
			time.sleep(10)
	except:
		print "Could not connect to that URL: "+str(fileno)
		tableEntry = 'File '+str(fileno)+'.xml\n'
		writeToFile(tableEntry, '_FilesWithError.txt', 'a')
		#quit()