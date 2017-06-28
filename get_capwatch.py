#!/usr/bin/env python
# A script for downloading CAPWATCH databases
# Requires: Mechanize (https://pypi.python.org/pypi/mechanize/)
# 
# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/capwatch_download
# 
import argparse
import mechanize

### Settings

login_url = 'https://www.capnhq.gov/CAP.eServices.Web/Default.aspx'
download_url = 'https://www.capnhq.gov/cap.capwatch.web/download.aspx'


### Function

def downloadCAPWATCH(username, password, organization, filename):
    """Download a CAPWATCH database
    
    :param username (str): eServices username
    :param password (str): eServices password
    :param organization (str): Organization ID
    :param filename (str): Filepath and name to write database to
    """
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
    try:
        browser['ctl00$MainContentPlaceHolder$OrganizationChooser1$ctl00'] =\
                    [organization]
        browser.submit()
    except:
        exit('Invalid or unauthorized organization')
    
    # Download the CAPWATCH zipfile
    browser.select_form('aspnetForm')
    browser.form.find_control('ctl00$MainContentPlaceHolder$btnSubmit').disabled = True
    browser.form.find_control('ctl00$MainContentPlaceHolder$btnReset').disabled = True
    browser.form.new_control('hidden', '__EVENTTARGET', {})
    browser.form.new_control('hidden', '__EVENTARGUMENT', {})
    browser.form.set_all_readonly(False)
    browser['__EVENTTARGET'] = 'ctl00$MainContentPlaceHolder$lnkGetData'
    browser['__EVENTARGUMENT'] = ''
    browser['ctl00$MainContentPlaceHolder$OrganizationChooser1$ctl00'] =\
                    [organization]
    resp = browser.submit()
    fileobj = open(filename,'wb')
    fileobj.write(resp.read())
    fileobj.close()


### Main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download CAPWATCH database')
    parser.add_argument('-u', '--username', help='eServices username',
                        required=True)
    parser.add_argument('-p', '--password', help='eServices password',
                        required=True)
    parser.add_argument('-o', '--organization', help='Organization ID',
                        required=True)
    parser.add_argument('-f', '--filename', help='Destination filename',
                        default='capwatch.zip')
    args = parser.parse_args()
    downloadCAPWATCH(args.username, args.password, args.organization, 
                     args.filename)
