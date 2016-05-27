import urllib2, urllib, sys, re, time, os, Queue, threading



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
        attempts = 0
        attemptLimit = 5
        while attempts <= attemptLimit:
                try:
                        data = urllib2.urlopen(input).read()
                        break
                except:
                        print "[-] Error opening download link...trying "+(5-attempts)+" more times..."
                        attempts += 1
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
		items.reverse()
		for item in items:
			title = re.findall("<title>(.+?)<\/title>", item)
			print "[+] Get title: "+title[0]
			dllink = re.findall("<enclosure url=\"(.+?)\".+?\/>", item, re.DOTALL)
			print "[+] Get URL"
			#supersizedURL = maketiny(dllink[0])
			title[0] = title[0].replace(":", "_")
			print "[+] Item:\n\tTitle: "+title[0]+"\n\tURL: "+dllink[0]+"\n"
			print "[+] Downloading item..."
			try:
				print "[+] Opening download link..."
				firstLevelLink = urllib2.urlopen(dllink[0])
				print "[+] Successfully opened download link..."
				print "[+] Reading first level..."
				firstread = firstLevelLink.read()
				print "[+] Successfully read first level..."
				print "[+] Attempting to get redirect link..."
				redirectURL = firstLevelLink.geturl()
			except urllib2.HTTPError, httperror:
				print "[-] ERROR :"
				print httperror
				print "[-] Error opening download link..."
				writeToFile(title[0]+"\n", ".\\"+dirName+"\\error.txt", "a")
				continue
			print "[+] Successfully opened download link..."
			print "[+] Getting redirect url..."
			print "[+] Redirect URL: "+redirectURL+"\n"
			try:
				print "[+] Opening redirect link..."
				content = urllib2.urlopen(redirectURL).read()
			except urllib2.HTTPError, httperror:
				print "[-] ERROR :"
				print httperror
				print "[-] Error opening redirect link..."
				writeToFile(title[0]+"\n", ".\\"+dirName+"\\error.txt", "a")
				continue
			print "[+] Successfully opened redirect link..."
			print "[+] Writing data to "+title[0]+".mp4..."
			writeToFile(content, '.\\'+dirName+'\\'+title[0]+'.mp4', 'wb')
			print "[+] Download complete!!!\n\n"
            #End loop
		print "\n\n\n[+] Successfully crawled and downloaded!!!\n\n\n"
		writeToFile("completed", '.\\'+dirName+'\\completed.txt', 'wb')
	except:
		print "Could not connect to that URL: "+str(fileno)
        #quit()


filenum1 = 0
filenum2 = 0
filenum3 = 0
filenum4 = 0
filenum5 = 0
filenum6 = 0
print "\n\nStart downloading...\n\n"

doIt(filenum1, "")


print "\n\n\nFinally completely downloaded everything!!!\n\n"

