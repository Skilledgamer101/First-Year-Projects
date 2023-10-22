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
MENU = (By.CSS_SELECTOR, "button[aria-label='Toggle Main Menu']")
SSC = (By.CSS_SELECTOR, "a[href = '/myAccount/studentSuccessCentre.htm']")
WORK = (By.CSS_SELECTOR, "a[href = '/myAccount/studentSuccessCentre/employment.htm']")
POSTINGS = (By.CSS_SELECTOR, "a[href = '/myAccount/studentSuccessCentre/employment/postings.htm']")
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


WebDriverWait(browser, 20).until(EC.element_to_be_clickable(MENU)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(SSC)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(MENU)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(WORK)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(MENU)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(POSTINGS)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(SPRING)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(BOX)).click()

WebDriverWait(browser, 20).until(EC.element_to_be_clickable(SEARCH)).click()

page_source = browser.page_source
soup = BeautifulSoup(page_source, 'lxml')
all = soup.select('td')
# first group in deadlineRegex matches DATE and second matches TIME (w/o unnecessary spaces)

IDRegex = re.compile(r'(\d\d\d\d\d\d)', re.I) 
dateRegex = re.compile(r'(\w+\s\d+,\s\d+)', re.I)
timeRegex = re.compile(r'(\d+:\d+\s\w+)', re.I)
new = all[5].getText().strip()
f = open("ssc.txt", "r")
last_job = f.read()
f.close()

i = 0
j = 0
message = ''
# just want role, company, openings, location, and deadline
# send all new jobs (after last seen)
while True:

    temp = IDRegex.search(all[i].getText())
    while temp == None:
        i += 1
        temp = IDRegex.search(all[i].getText())
    # will reach here after finding ID number of job and the associated index in ALL

    # get other relevant details of this job from ALL variable
    role = all[i + 1].getText().strip()
    if role == last_job:
        break
    company = all[i + 2].getText()
    openings = all[i + 5].getText()
    location = all[i + 6].getText()
    deadline = all[i + 10].getText()
    # get date and time from deadline
    date = dateRegex.search(deadline).group()
    time = timeRegex.search(deadline).group()
    deadline = date + " " + time
    message += f"Role: {role}\nCompany: {company}\nOpenings: {openings}\nLocation: {location}\nDeadline: {deadline}"
    message += '\n\n'

    # inc i so same id not reused
    i += 12
    # if we have reached the end of jobs

    if i == len(all):
        message = "Unfortunately the last seen job has been removed and the program cannot judge whether these jobs are new or not\n\n" + message
        break

# send email if new jobs
if message != '':
    ezgmail.send(recipient, 'New SSC Jobs', message)
    print(f"SSC Email sent with message\n\n{message}\n\n")
else:
    ezgmail.send(recipient, 'No new SSC jobs till now (EOM)', 'Inshallah')
    print("SSC Email sent (no new jobs)\n\n")
# set last seen to new
f = open("ssc.txt", "w")
f.write(new)
f.close()
