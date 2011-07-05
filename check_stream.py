#!/usr/bin/env python
# Author: Gaurav Ghimire (gaurav.ghimire@gmail.com)
# Date: 2nd July 2011
import urllib2,sys,os
from elementtree import ElementTree as ET
# for python 2.5 and later comment the line above and uncomment the one below
# from xml.etree import ElementTree as ET


##Variable Definitions###
# URL = the location of the url with connection stats
# username = Username for the portal
# password = Password for the portal 
# xmlpath = location of the file where you want the status be written

url = "http://example.com:8086/connectioncounts"
username = "user"
password = "password"
xmlpath = os.path.abspath("/usr/local/nagios/libexec/conncunt.xml")

def getPage(url):
    """This function retrieves the xml object from the web page and writes it to a filename called conncount.xml"""
    try:
		# Creating the HTTP auth handlers 
		passwdmngr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passwdmngr.add_password(None,url,username,password)
		authhandler = urllib2.HTTPDigestAuthHandler(passwdmngr)
		request = urllib2.build_opener(authhandler)
		urllib2.install_opener(request)
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)
		# Writing to the file
		xmlfile = open(xmlpath, "w")
		xmlfile.write(res.read())
		xmlfile.close()
    except urllib2.HTTPError:
		print "CRITICAL, resource page not found or forbidden"
		sys.exit(2)
    except urllib2.URLError:
		print "CRITICAL, Wrong DNS name or service name"
		sys.exit(2)

def getStatus(stream_name):
	# Retrieve and write the xml file
	getPage(url)
	# Define the xmltree
	xmltree = ET.parse(xmlpath)
	root = xmltree.getroot()
	# Define data values
	vhost = root.find("VHost")
	for app in vhost:
		for apps in app:
			if app.getchildren()[0].text == stream_name:
				for inst in apps:
						if len(apps.getchildren()) < 9:
							print "CRITICAL, %s stream not alive" % ( stream_name)
							sys.exit(2)
						elif len(inst.getchildren()) > 0:
							print "Status: OK, %s Total Sessions: %s" % ( stream_name, inst.getchildren()[6].text)
							sys.exit(0)

	print "CRITICAL: Stream not found in the server"
	sys.exit(2)

def main():
	if len(sys.argv) == 1:
		print "Usage: ./check_stream.py $streamname"
		sys.exit()
	else:
		getStatus(sys.argv[1])

if __name__ == "__main__":
	main()

