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
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from msedge.selenium_tools import Edge, EdgeOptions as Options
from chromeHider import HiddenChromeWebDriver
import time

if( sys.path[0] != os.getcwd() ):
    #Make them match by moving the Current Working Directory
    os.chdir(sys.path[0]);
#END IF

#!! More than 8 zip codes will cause the browser to have to be rest (Giant limits # of checks) and it'll add some time to the check, that's it it's really no big deal!!
zipper = ['5DIGZIP']; #zipcode to look for, separate by commas like ['55555','44444','33333'] if multiple (Giant only checks ?within 10 miles of zipcode?)

resendLimit = 60; #minutes, time limit until a new email can be sent
email = ''; #sender [email@provider.xxx]
password = ''; #sender pw [modern emails probably will require you to get a "1 time use" password or something like that for old apps, it'll be a rando string the site gives you]
destinations = ['']; #destination - comma separate for multiple destinations like ['yaboi@sk.ny','3993939393@bellmsg.old'] [you can text phones through ###@cellprovider.xxx google to see your cell provider's setup]

# giantFile = 'giantSource.txt'; #set name for the cache file
giantHard = 'https://giantfoodsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory'; #set giant hard-coded fallback [only link]
driverDelay = 15; #sec, time to wait while the chatbox tries to load - takes like 3 sec usually
fakeBrowser = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}; #get
giantReturn = requests.get(giantHard,headers=fakeBrowser).text; #get the text of the webpage# 

giantSet = {
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
options.add_argument('--disable-popup-blocking')
prefs = {"profile.default_content_setting_values.cookies" : 1, "profile.block_third_party_cookies" : False}
# add prefs 
options.add_experimental_option("prefs", prefs)

currentTime = datetime.datetime.today(); #get the time now
#Get the last time sent
if( Path('timez_giant.pkl').is_file() ):
    with open('timez_giant.pkl', 'rb') as filez:
        lastTime = pickle.load(filez); #get that time
    #END WITH
else:
    lastTime = datetime.datetime(1970,1,1); #set long time ago if never sent before
#END IF

if( (currentTime - lastTime).total_seconds() > 60*resendLimit ):

    giantWords = []; #prep this
    # if( (strstr(giantReturn,'Cloudflare').size == 0) & (strstr(giantReturn,'403 Forbidden').size == 0) ):
    #     try:
    #         k = strstr(giantReturn,'https://www.astutebot.com/chat/')[0]; #get where the link starts
    #         k2 = strstr(giantReturn[k:],'" style="display')[0]; #get where link ends
    #         giantCheck = giantReturn[k:k+k2]; #get the link from the dynamic site
    #     except:
    #         giantCheck = giantHard; #use hardcoded option
    #     #END IF
    # else:
    #     giantCheck = giantHard; #use hardcoded option
    # #END IF
    giantCheck = giantHard; #for giant no extra bonus site that might change
    
    # giantReturn = requests.get(giantCheck,headers=fakeBrowser).text; #get the text of the webpage
    #---chrome---
    # driver = HiddenChromeWebDriver(options=options); #hides window
    # driver = webdriver.Chrome(options=options); #default chrome call 
    #---edge---
    # driver = Edge('msedgedriver.exe',options=options); #specify name b/c new edge, open browser
    # driver = Edge();    
    #---firefox---
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.set_headless()
    #driver = webdriver.Firefox(firefox_options=fireFoxOptions)

    # driver.set_window_size(1554,842); #rando size under 1080p
    # driver.get(giantCheck); #open that link
    # driver.switch_to.frame(driver.find_element_by_name("botFrame")); #move to the frame
    driver = []; #make python happy
    try:        
        cntr = 11; #cnt something
        for i in range(0,len(zipper)):
            if( cntr > 7 ):
                #close it all, reopen it all
                if( i != 0 ):
                    driver.quit()
                    time.sleep(0.5); #give the page a chance to do stuff
                #END IF
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
                driver.get(giantCheck); #open that link
                
                WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Set Location')]")));
        
                #hard ot navigate site, so just yolo and code extra double inefficient
                ids = driver.find_elements_by_xpath('//*[@id]'); #get all element ids
                cntr = 0; #prep
                for j in ids:
                    #print j.tag_name
                    # print(j.get_attribute('id')); # id name as string
                    #--- Zip ---
                    if( strstr(j.get_attribute('id'),'zip-input').size > 0 ):
                        idNum_zip = cntr; #set 
                    #END IF
                    cntr += 1; #increment
                #END FOR j
                
                #--- Scroll down to fit it all on the page ---
                button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Go')]")[-1]; #search for elements with this string
                try:
                    button2click.click(); #click it
                except:
                    pass; #trying to click next raises an error but scrolls down to the next button, sick hacks?
                #END TRY
                
                cntr = 0; #reset
            #END IF
            
            #--- Zip ---
            button2click = ids[idNum_zip]; #get it
            button2click.click(); #click it
            actions = ActionChains(driver); #fire up the actions
            actions.send_keys(Keys.BACKSPACE*10).perform(); #delete anything there
            actions = ActionChains(driver); #fire up the actions
            actions.send_keys(zipper[i]).perform(); #write in the zip
            
            button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Go')]")[-1]; #search for elements with this string
            try:
                button2click.click(); #click it
            except:
                button2click.click(); #click it again idk
            #END TRY
            
            time.sleep(0.15); #give the page a chance to do stuff
            wrongZip = driver.find_elements_by_xpath("//*[contains(text(), 'ZIP code does not exist')]"); #search for elements with this string
            noLoc = driver.find_elements_by_xpath("//*[contains(text(), 'There are no locations')]"); #search for elements with this string
            maxZipz = driver.find_elements_by_xpath("//*[contains(text(), 'Maximum zip code search')]"); #search for elements with this string

            if( len(maxZipz) == 0 ):
                if( (len(wrongZip) == 0) & (len(noLoc) == 0) ):
                    #if it doesn't tell you zip wrong and no locations, that must be avail? I couldn't test a positive case so gotta go negative
                    giantSet['all reserved'] = False; #all reserved stays true, no appointments
                    driver.save_screenshot('giantAvail.png'); #save a pic to check later
                    giantWords.append(zipper[i]); #add the zip code on
                #END IF
            #END IF
            
            cntr += 1; #increment
        #END FOR i
    except:
        # giantSet['all reserved'] = True; #all reserved stays true, no appointments
        driver.save_screenshot('giantNotSeenBefore.png'); #save a pic to check later
    #END TRY
    # driver.save_screenshot('giantTest.png'); #save a pic to check later
    # try:
    #     myElem = WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'are reserved at this time')]")));
    #     giantSet['all reserved'] = True; #all reserved stays true, no appointments
    # except TimeoutException:
    #     giantSet['all reserved'] = True; #all reserved stays true, no appointments
    #     driver.save_screenshot('giantNotSeenBefore.png'); #save a pic to check later
    # #END TRY
    driver.quit()
    # giantReturns = driver.find_elements_by_xpath("//*[contains(text(), 'are reserved at this time')]"); #search for elements with this string
    
    if( (giantSet['all reserved'] == False) ):
        #time to send email if either pass this
        subject = 'giant Site Active'; #subject line
        message = 'Body: giant at zipcode(s) '+' & '.join(giantWords)+' has availability. Site: '+giantCheck; #message body
        
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
        print('SENT AM EMAIL')
        
        with open('timez_giant.pkl', 'wb') as filez:
            pickle.dump(currentTime, filez); #record the time sent
        #END WITH
    #END IF
    
    
    # if( giantReturn != giantOld ): #reduce overwrite of same thing
    #     with open(giantFile, 'w') as gianter:
    #         gianter.write(giantReturn); #write in the source code of the webpage
    #     #END WITH
    # #END IF
#END IF




























