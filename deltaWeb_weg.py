from pathlib import Path
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import pickle
from strstr import strstrNB as strstr
import sys, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
#from msedge.selenium_tools import Edge, EdgeOptions as Options
from chromeHider import HiddenChromeWebDriver
import time

if( sys.path[0] != os.getcwd() ):
    #Make them match by moving the Current Working Directory
    os.chdir(sys.path[0]);
#END IF

stater = 'PA'; #state to look for
resendLimit = 60; #minutes, time limit until a new email can be sent
email = ''; #sender [email@provider.xxx]
password = ''; #sender pw [modern emails probably will require you to get a "1 time use" password or something like that for old apps, it'll be a rando string the site gives you]
destinations = ['','']; #destination - comma separate for multiple destinations like ['yaboi@sk.ny','3993939393@bellmsg.old'] [you can text phones through ###@cellprovider.xxx google to see your cell provider's setup]

# wegFile = 'wegSource.txt'; #set name for the cache file
wegHard = 'https://www.astutebot.com/chat/index.aspx?aid=rl2qitSwmTOL14InJowW8Q'; #set weg hard-coded fallback [only link]
driverDelay = 15; #sec, time to wait while the chatbox tries to load - takes like 3 sec usually
fakeBrowser = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}; #get
wegReturn = requests.get('https://www.wegmans.com/covid-vaccine-registration/',headers=fakeBrowser).text; #get the text of the webpage# 

wegSet = {
    'all reserved':True, #default to true that 'are reserved at this time' is there
    }; #prep a dict


options = Options(); #make edge options
#--for edge only--
# options.use_chromium = True
# options.add_argument('headless')
# options.add_argument('disable-gpu')
#--for chrome only--
# options.add_argument("--disable-extensions")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1554,842")
prefs = {"profile.default_content_setting_values.cookies" : 1, "profile.block_third_party_cookies" : False}
# add prefs 
options.add_experimental_option("prefs", prefs)

currentTime = datetime.datetime.today(); #get the time now
#Get the last time sent
if( Path('timezWeg.pkl').is_file() ):
    with open('timezWeg.pkl', 'rb') as filez:
        lastTime = pickle.load(filez); #get that time
    #END WITH
else:
    lastTime = datetime.datetime(1970,1,1); #set long time ago if never sent before
#END IF

if( (currentTime - lastTime).total_seconds() > 60*resendLimit ):

    # wegWords = []; #prep this
    if( (strstr(wegReturn,'Cloudflare').size == 0) & (strstr(wegReturn,'403 Forbidden').size == 0) ):
        try:
            k = strstr(wegReturn,'https://www.astutebot.com/chat/')[0]; #get where the link starts
            k2 = strstr(wegReturn[k:],'" style="display')[0]; #get where link ends
            wegCheck = wegReturn[k:k+k2]; #get the link from the dynamic site
        except:
            wegCheck = wegHard; #use hardcoded option
        #END IF
    else:
        wegCheck = wegHard; #use hardcoded option
    #END IF
    wegCheck = wegHard; #for weg no extra bonus site that might change
    
    # wegReturn = requests.get(wegCheck,headers=fakeBrowser).text; #get the text of the webpage
    #---chrome---
    driver = HiddenChromeWebDriver(options=options); #hides window
    # driver = webdriver.Chrome(options=options); #default chrome call 
    #---edge---
    # driver = Edge('msedgedriver.exe',options=options); #specify name b/c new edge, open browser
    # driver = Edge();    
    #---firefox---
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.set_headless()
    #driver = webdriver.Firefox(firefox_options=fireFoxOptions)

    driver.set_window_size(1554,842); #rando size under 1080p
    driver.get(wegCheck); #open that link
    # driver.switch_to.frame(driver.find_element_by_name("botFrame")); #move to the frame
    try:
        WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Get Started')]")));
        button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Get Started')]")[0]; #search for elements with this string
        button2click.click(); #click it
        try:
            WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Please select your state')]")));
            
            try:
                WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), stater)]")));
            
                button2click = driver.find_elements_by_xpath("//*[contains(text(), stater)]")[-1]; #search for elements with this string
    
                # #this code is for debug, it highlights the button
                # element = button2click
                # driverEle = element._parent
                # def apply_style(s):
                #     driverEle.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)
                # original_style = element.get_attribute('style')
                # apply_style("background: yellow; border: 2px solid red;")
                # driver.save_screenshot('wegTest.png')
                # time.sleep(.8)
                # apply_style(original_style)
                
                button2click.click(); #click it
                # webdriver.common.action_chains.ActionChains(driver).move_to_element(button2click).click().perform()
                # action = webdriver.common.action_chains.ActionChains(driver)
                # buttonSize = button2click.size;
                # # action.move_to_element_with_offset(button2click, buttonSize['width']//4, buttonSize['height']//4)
                # action.move_to_element_with_offset(button2click, 0, 0)
                # action.click()
                # action.perform()
                
                try:
                    WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'are reserved at this time')]")));
                    wegSet['all reserved'] = True; #all reserved stays true, no appointments
                    # driver.save_screenshot('wegTest.png'); #save a pic to check later
                except TimeoutException:
                    wegSet['all reserved'] = False; #set all reserved to false, might be appointments
                    driver.save_screenshot('wegNotReserved.png'); #save a pic to check later
                #END TRY
            except TimeoutException:
                wegSet['all reserved'] = True; #all reserved stays true, no appointments
            #END TRY
            
        except TimeoutException:
            wegSet['all reserved'] = True; #all reserved stays true, no appointments
            # driver.save_screenshot('wegNotSeenBefore.png'); #save a pic to check later
        #END TRY
    except:
        wegSet['all reserved'] = True; #all reserved stays true, no appointments
        driver.save_screenshot('wegNotSeenBefore.png'); #save a pic to check later
    #END TRY
            
    # try:
    #     myElem = WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'are reserved at this time')]")));
    #     wegSet['all reserved'] = True; #all reserved stays true, no appointments
    # except TimeoutException:
    #     wegSet['all reserved'] = True; #all reserved stays true, no appointments
    #     driver.save_screenshot('wegNotSeenBefore.png'); #save a pic to check later
    # #END TRY
    driver.quit()
    # wegReturns = driver.find_elements_by_xpath("//*[contains(text(), 'are reserved at this time')]"); #search for elements with this string
    
    if( (wegSet['all reserved'] == False) ):
        #time to send email if either pass this
        subject = 'Weg Site Active'; #subject line
        message = 'Body: Weg does not say all reserved. Site: '+wegCheck; #message body
        
        msg = MIMEMultipart(); #start an email message
        msg['From'] = email; #set from
        msg['To'] = ', '.join(destinations); #set to
        msg['Subject'] = subject; #set subject
        
        msg.attach(MIMEText(message, 'plain')); #set message
        
        server = smtplib.SMTP('SMTPSERVERFOREMAIL.something', 000); #set the server, set the port number
        server.starttls(); #use STARTTLS
        server.login(email, password); #login
        text = msg.as_string(); #prep the email
        server.sendmail(email, destinations, text); #send the email
        server.quit(); #kill the connection
        
        with open('timezWeg.pkl', 'wb') as filez:
            pickle.dump(currentTime, filez); #record the time sent
        #END WITH
    #END IF
    
    
    # if( wegReturn != wegOld ): #reduce overwrite of same thing
    #     with open(wegFile, 'w') as weger:
    #         weger.write(wegReturn); #write in the source code of the webpage
    #     #END WITH
    # #END IF
#END IF




























