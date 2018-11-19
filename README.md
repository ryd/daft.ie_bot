# daft.ie_bot
Notification Bot for daft.ie

# Description
Notification bot for daft.ie listings. Finding an apartment in Ireland can be taff. This bot allows you to simplify the procedure finding an apartment by mailing you new offers quickly. Already mailed listing will be cached to avoid double work. Criteria can be defined in a config file. Automating this script in a crontab allows you to react quickly on new listings.

# Installing
The script has a dependency to python3 as well as one module.

'''
pip3 install daftlistings html2text
'''

If you want to start your script on regular basis, check out crontab man page.

# Configuration
The configuration for the bot is stored in a file called config.txt

* email_address - your email address
* email_user - SMTP authenticaton user
* email_password - SMTP authentication password
* email_server - hostname of your SMTP server
* email_port - SMTP server port
* email_subject - Email subject

* rent_max_price - maximum rent of listings
* rent_min_bedroom - minimal number of bed rooms
* rent_max_bedroom - maximal number of bed rooms
* rent_area - list of districts to list
* rent_county - region, usually "dublin"

# Finding your area
The area is a list, seperated by comma, of districts to include in the search. This list can be archived by visiting daft.ie and start an advanced search. In the URL, the value after residential-property-for-rent/ *HERE* /? is your choosen areas.

# Licence
See LICENCE file

# Credits
* TOG Dublin Hackerspace - https://www.tog.ie/
* Anthony Bloomer - https://github.com/AnthonyBloomer

Happy apartment hunting.




