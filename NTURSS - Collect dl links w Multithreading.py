import urllib2, urllib, sys, re, time, Queue, threading



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

def doIt(fileno, dirName):
        try:
                filenostr = str(fileno)
                print '\n\n\n[+] Searching for File '+filenostr+'.xml : '
                data = requestURL(filenostr)
                # Replace all &amp; to &
                newdata = data.replace("&amp;", "&")
                print '[+] Successfully requested URL'
                #<title>15S1-L6115</title>
                #title = re.findall("<a rel=\"nofollow\" target=\"_blank\" 	href=\"(.+?)\">.+?<\/a>",data)
                #title = re.findall("<title>(.+?)<\/title>",data)
                #writeToFile(data, "original.txt", "w")
                #writeToFile(newdata, "new.txt", "w")
                items = re.findall(r'<item>(.+?)<\/item>', newdata, re.DOTALL)
                #print "\n\ntest\n"+items[0]+"\nendtest\n\n"
                # Loop starts here
                for item in items:
                        title = re.findall("<title>(.+?)<\/title>", item)
                        print "[+] Get title: "+title[0]
                        dllink = re.findall("<enclosure url=\"(.+?)\".+?\/>", item, re.DOTALL)
                        print "[+] Get URL"
                        #supersizedURL = maketiny(dllink[0])
                        title[0] = title[0].replace(":", "_")
                        print "\n[+] Item:\n\tTitle: "+title[0]+"\n\tURL: "+dllink[0]+"\n"
                        print "[+] Downloading item...\n"
                        redirectURL = urllib2.urlopen(dllink[0]).geturl()
                        print "[+] Redirect URL: "+redirectURL+"\n"
                        content = urllib2.urlopen(redirectURL).read()
                        writeToFile(content, '.\\'+dirName+'\\'+title[0]+'.mp4', 'wb')
                        print "[+] Download complete!!!\n\n"
                        #End loop
                print "\n\n\n[+] Successfully crawled and downloaded!!!\n\n\n"
        except:
                print "Could not connect to that URL: "+str(fileno)
                #quit()



filenum1 = 0
filenum2 = 0
filenum3 = 0
filenum4 = 0
filenum5 = 0
filenum6 = 0
q = Queue.Queue()

print "\n\nStart downloading...\n\n"
t1 = threading.Thread(target=doIt, args = (filenum1, ""))
t2 = threading.Thread(target=doIt, args = (filenum2, ""))
t3 = threading.Thread(target=doIt, args = (filenum3, ""))
t4 = threading.Thread(target=doIt, args = (filenum4, ""))
t5 = threading.Thread(target=doIt, args = (filenum5, ""))
t6 = threading.Thread(target=doIt, args = (filenum6, ""))
t1.start()
t2.start()
t3.start()
t4.start()
t6.start()
t6.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()

print "\n\n\nFinally completely downloaded everything!!!\n\n"

