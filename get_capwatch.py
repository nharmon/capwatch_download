# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/capwatch_download
# 
# A script for downloading CAPWATCH databases
# 
import mechanize

################
### Settings ###
################

# This is your CAP eServices Username (most likely your CAPID)
username = '000000'

# This is your CAP eServices Password
password = 'password'

# This is the organization ID whose data you are downloading, you can find
# the ID by looking at the source of the download URL (see below)
orgid = '0'

# The path and filename where to write the CAPWATCH zip file.
outfilename = 'capwatch.zip'

login_url = 'https://www.capnhq.gov/CAP.eServices.Web/Default.aspx'
download_url = 'https://www.capnhq.gov/cap.capwatch.web/download.aspx'

#######################
### End of Settings ###
#######################

# Login to eServices
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.open(login_url)
browser.select_form('form1')
browser.form['Login1$UserName'] = username
browser.form['Login1$Password'] = password
browser.submit()

# Prepare the CAPWATCH Download
browser.open(download_url)
browser.select_form('aspnetForm')
browser['ctl00$MainContentPlaceHolder$OrganizationChooser1$ctl00'] = [orgid]
browser.submit()

# Download the CAPWATCH zipfile
browser.select_form('aspnetForm')
browser.form.find_control('ctl00$MainContentPlaceHolder$btnSubmit').disabled = True
browser.form.find_control('ctl00$MainContentPlaceHolder$btnReset').disabled = True
browser.form.new_control('hidden', '__EVENTTARGET', {})
browser.form.new_control('hidden', '__EVENTARGUMENT', {})
browser.form.set_all_readonly(False)
browser['__EVENTTARGET'] = 'ctl00$MainContentPlaceHolder$lnkGetData'
browser['__EVENTARGUMENT'] = ''
browser['ctl00$MainContentPlaceHolder$OrganizationChooser1$ctl00'] = [orgid]
resp = browser.submit()
fileobj = open(outfilename,'wb')
fileobj.write(resp.read())
fileobj.close()
