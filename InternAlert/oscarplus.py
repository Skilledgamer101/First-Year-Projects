from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import ezgmail
import re

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")
SPRING = (By.CSS_SELECTOR, "a[href = '#runMultipleSearchesDialog']")
BOX = (By.CSS_SELECTOR, "input[type = 'checkbox']")
SEARCH = (By.CSS_SELECTOR, "button[type = 'submit']")

path = input("Please enter the full path to chromedriver:\n")
path.encode('unicode_escape')
browser = webdriver.Chrome(path, chrome_options = options)
browser.get('https://www.oscarplusmcmaster.ca/Shibboleth.sso/Login?entityID=https://sso.mcmaster.ca/idp/shibboleth&target=https://www.oscarplusmcmaster.ca/secure/ssoStudent.htm')

# wait for email field and enter email
email = input("Please enter your McMaster email address:\n")
password = input("Please enter your McMaster password:\n")
recipient = input("Please enter the email address you want to send the jobs to:\n")
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(email)

# Click Next
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

# wait for password field and enter password
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)

# Click Login - same id?
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

# Stay signed in
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

# Logged into OscarPlus
# Now just redirect to job posting page

browser.get("https://www.oscarplusmcmaster.ca/myAccount/eng/coop/postings.htm")

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(SPRING)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(BOX)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(SEARCH)).click()

page_source = browser.page_source
soup = BeautifulSoup(page_source, 'lxml')
all = soup.select('td')
if all == None:
    message = "No OscarPlus jobs exist in the search"
    ezgmail.send(recipient, 'No OscarPlus jobs exist in the search', message)
    print("\n\nNo OscarPlus jobs exist in the search\n\n")
    exit(0)
elems = soup.select('td[data-totitle]')
durationRegex = re.compile(r'\d{1,}-month')
# first group in deadlineRegex matches DATE and second matches TIME (w/o unnecessary spaces) 
dateRegex = re.compile(r'(\w+\s\d+,\s\d+)', re.I)
timeRegex = re.compile(r'(\d+:\d+\s\w+)', re.I)
new = elems[0].get('data-totitle')
f = open("coop.txt", "r")
last_job = f.read()
f.close()

i = 0
j = 0
message = ''
titles = ['Role: ', 'Company: ', 'Division: ']
# send all new jobs (after last seen)
while elems[i].get('data-totitle') != last_job:
    
    message += (titles[i % 3] + (elems[i].get('data-totitle')) + '\n')
    # if next entry (in next iteration) is going to be a new role
    if i % 3 == 2:
        
        duration = durationRegex.search(all[j].getText())
        # search text of each td element till we find duration
        while duration == None:
            j += 1
            duration = durationRegex.search(all[j].getText())
        # after finding duration, get actual text
        duration = duration.group()
        #location, applications, and app deadline right after location
        location = all[j + 1].getText()
        applications = all[j + 2].getText()
        deadline = all[j + 3].getText()
        date = dateRegex.search(deadline).group()
        time = timeRegex.search(deadline).group()
        deadline = date + " " + time
        # put j on non-duration text so it doesn't reuse current in next iteration
        j += 1
        # add duration, location...
        message += f"Duration: {duration}\nLocation: {location}\nApplications: {applications}\nDeadline: {deadline}"
        message += '\n\n'
    i += 1
    # if we have reached the end of jobs in BS obj
    if i == len(elems):
        message = "Unfortunately the last seen job has been removed and the program cannot judge whether these jobs are new or not\n\n" + message
        break

# send email if new jobs
if message != '':
    ezgmail.send(recipient, 'New OscarPlus Jobs', message)
    print(f"OSCARPLUS Email sent with message\n\n{message}\n\n")
else:
    ezgmail.send(recipient, 'No new OSCARPLUS jobs till now (EOM)', 'Hopefully soon :)')
    print("OSCARPLUS Email sent (no new jobs)\n\n")
# set last seen to new
f = open("coop.txt", "w")
f.write(new)
f.close()
