#!python3

# this script does not need any parameter. For testing purpose, you can give two parameters
# python3 daft_bot.py <config_file> <cache_file>

import sys, smtplib, email
try:
	from daftlistings import Daft, SortOrder, SortType, RentType
except:
	print("[E] daftlisting dependency missing.")
	print("Run: pip3 install daftlistings html2text")
	sys.exit(-1)
from email.message import EmailMessage

# check version
if sys.version_info[0] < 3:
	print("[E] This script is only compatible with Python 3 or higher.")
	sys.exit(-1)

# read and parse config file
config = {}
config_file = 'config.txt'
if len(sys.argv) > 1:
	config_file = sys.argv[1]
	print("[*] Using %s as config file." % config_file)
try:
	with open(config_file) as file:
		lines = file.readlines()
	for line in lines:
		line = line.strip()
		if line and line[0] != '#':
			s = line.split('=', maxsplit=1)
			config[s[0]] = int(s[1]) if s[1].isdigit() else s[1]
except:
	print("[E] Unable to read or parse config file.")
	sys.exit(-1)

# set parameter
fromAddr = config["email_address"]
toAddrs = config["email_address"]
cachefile = 'listings.txt'
if len(sys.argv) > 2:
	cachefile = sys.argv[2]
	print("[*] Using %s as cache file." % cachefile)

# load cache if exists
print("[*] Loading Cache.")
cached = {}
try:
	f = open(cachefile, 'r')
	for i in f.readlines():
		cached[i.strip()] = ""
	f.close()
except:
	print("[W] Unable to read cache file. Don't worry if you start from scretch.")

# search listings on daft
print("[*] Reading Daft.")
listings = []
offset = 0
daft = Daft()
try:
	daft.set_county(config["rent_county"])
	daft.set_area(config["rent_area"])
	daft.set_listing_type(RentType.ANY)
	daft.set_max_price(config["rent_max_price"])
	daft.set_min_beds(config["rent_min_bedroom"])
	daft.set_max_beds(config["rent_max_bedroom"])
except:
	print("[E] Configuration is broken.")
	sys.exit(-1)
while True:
	l = daft.search()
	if len(l) == 0:
		break
	for listing in l:
		if listing.daft_link in cached:
			continue
		listings.append(listing)
		cached[listing.daft_link] = ''
	offset += 20
	daft.set_offset(offset)
print("[*] %d new listing(s) found." % len(listings))

# if we have new entries, mail them and update cache
if len(listings) > 0:
	text = "%d new ad(s) found.\n" % (len(listings))
	for i in listings:
		text += "-----\n%s\n%s\n%s\n" % (i.formalised_address, i.daft_link, i.price)
	msg = EmailMessage()
	msg['From'] = "Daft Notification <%s>" % config["email_address"]
	msg['To'] = config["email_address"]
	msg['Subject'] = config["email_subject"]
	msg['Date'] = email.utils.formatdate()
	msg.set_content(text)

	try:
		server = smtplib.SMTP(config["email_server"], config["email_port"])
	except:
		print("[E] Unable to connect to email server, please check config.")
		sys.exit(-1)
	#server.set_debuglevel(True)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(config["email_user"], config["email_password"])
	server.sendmail(fromAddr, toAddrs, msg.as_string(unixfrom=True))
	server.quit()
	print("[*] Email Send.")

	try:
		f = open(cachefile, 'w')
		for i in cached.keys():
			f.write("%s\n" % i)
		f.close()
		print("[*] Cache updated.")
	except:
		print("[E] Unable to write cache file.")
		sys.exit(-1)

# exit
print("[*] Finished.")
