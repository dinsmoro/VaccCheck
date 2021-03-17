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

fakeBday = 'DY/MO/YEAR'; #put in a fake bday, put something near yours but not yours for secret - when you actually sign up use your real one
city = 'TOWN'; #town/city around where you want to look
stater = 'PA'; #state to look for
zipper = '5DIGZIP'; #zipcode to look for
occupation = 'None of the Above'; #get a list of possible things to put from https://www.riteaid.com/pharmacy/covid-qualifier
medcond = 'None of the Above'; #get a list of possible things to put from https://www.riteaid.com/pharmacy/covid-qualifier


resendLimit = 60; #minutes, time limit until a new email can be sent
email = ''; #sender [email@provider.xxx]
password = ''; #sender pw [modern emails probably will require you to get a "1 time use" password or something like that for old apps, it'll be a rando string the site gives you]
destinations = ['']; #destination - comma separate for multiple destinations like ['yaboi@sk.ny','3993939393@bellmsg.old'] [you can text phones through ###@cellprovider.xxx google to see your cell provider's setup]

# riteaidFile = 'riteaidSource.txt'; #set name for the cache file
riteaidHard = 'https://www.riteaid.com/pharmacy/covid-qualifier'; #set riteaid hard-coded fallback [only link]
driverDelay = 15; #sec, time to wait while the chatbox tries to load - takes like 3 sec usually
fakeBrowser = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}; #get
riteaidReturn = requests.get(riteaidHard,headers=fakeBrowser).text; #get the text of the webpage# 

riteaidSet = {
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
if( Path('timez_riteaid.pkl').is_file() ):
    with open('timez_riteaid.pkl', 'rb') as filez:
        lastTime = pickle.load(filez); #get that time
    #END WITH
else:
    lastTime = datetime.datetime(1970,1,1); #set long time ago if never sent before
#END IF

if( (currentTime - lastTime).total_seconds() > 60*resendLimit ):

    riteaidWords = []; #prep this
    # if( (strstr(riteaidReturn,'Cloudflare').size == 0) & (strstr(riteaidReturn,'403 Forbidden').size == 0) ):
    #     try:
    #         k = strstr(riteaidReturn,'https://www.astutebot.com/chat/')[0]; #get where the link starts
    #         k2 = strstr(riteaidReturn[k:],'" style="display')[0]; #get where link ends
    #         riteaidCheck = riteaidReturn[k:k+k2]; #get the link from the dynamic site
    #     except:
    #         riteaidCheck = riteaidHard; #use hardcoded option
    #     #END IF
    # else:
    #     riteaidCheck = riteaidHard; #use hardcoded option
    # #END IF
    riteaidCheck = riteaidHard; #for riteaid no extra bonus site that might change
    
    # riteaidReturn = requests.get(riteaidCheck,headers=fakeBrowser).text; #get the text of the webpage
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
    driver.get(riteaidCheck); #open that link
    # driver.switch_to.frame(driver.find_element_by_name("botFrame")); #move to the frame
    try:
        WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Zip Code')]")));
        
        #hard ot navigate site, so just yolo and code extra double inefficient
        ids = driver.find_elements_by_xpath('//*[@id]'); #get all element ids
        cntr = 0; #prep
        for i in ids:
            #print i.tag_name
            # print(i.get_attribute('id')); # id name as string
            #--- DOB ---
            if( strstr(i.get_attribute('id'),'calender').size > 0 ):
                idNum_dob = cntr; #set 
            #END IF
            #--- City ---
            if( strstr(i.get_attribute('id'),'city').size > 0 ):
                idNum_city = cntr; #set 
            #END IF
            #--- State ---
            if( strstr(i.get_attribute('id'),'eligibility_state').size > 0 ):
                idNum_state = cntr; #set 
            #END IF
            #--- Zip ---
            if( strstr(i.get_attribute('id'),'zip').size > 0 ):
                idNum_zip = cntr; #set 
            #END IF
            #--- Occupation ---
            if( strstr(i.get_attribute('id'),'Occupation').size > 0 ):
                idNum_occ = cntr; #set 
            #END IF
            #--- Medical Condition ---
            if( strstr(i.get_attribute('id'),'mediconditions').size > 0 ):
                idNum_med = cntr; #set 
            #END IF
            cntr += 1; #increment
        #END FOR i
        
        #--- Scroll down to fit it all on the page ---
        button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")[0]; #search for elements with this string
        try:
            button2click.click(); #click it
        except:
            pass; #trying to click next raises an error but scrolls down to the next button, sick hacks?
        #END TRY
        
        #--- DOB ---
        button2click = ids[idNum_dob]; #get it
        button2click.click(); #click it
        actions = ActionChains(driver); #fire up the actions
        actions.send_keys(fakeBday).perform(); #write in the DOB
        
        #--- City ---
        button2click = ids[idNum_city]; #get it
        button2click.click(); #click it
        actions = ActionChains(driver); #fire up the actions
        actions.send_keys(city).perform(); #write in the city
        
        #--- State ---
        button2click = ids[idNum_state]; #get it
        button2click.click(); #click it
        button2click.click(); #click it again
        actions = ActionChains(driver); #fire up the actions
        actions.send_keys(stater).perform(); #write in the stater
        buttonSize = button2click.size;
        actions = ActionChains(driver); #fire up the actions
        actions.move_to_element_with_offset(button2click, buttonSize['width']//2, 3*buttonSize['height']//2);
        actions.click();
        actions.perform();
        
        #--- Zip ---
        button2click = ids[idNum_zip]; #get it
        button2click.click(); #click it
        actions = ActionChains(driver); #fire up the actions
        actions.send_keys(zipper).perform(); #write in the city
        
        #--- Occupation ---
        button2click = ids[idNum_occ]; #get it
        button2click.click(); #click it
        button2click.click(); #click it again
        actions = ActionChains(driver); #fire up the actions
        actions.send_keys(occupation).perform(); #write in the occ
        buttonSize = button2click.size;
        actions = ActionChains(driver); #fire up the actions
        actions.move_to_element_with_offset(button2click, buttonSize['width']//2, 3*buttonSize['height']//2);
        actions.click();
        actions.perform();
        
        #--- Medical Condition ---
        button2click = ids[idNum_med]; #get it
        button2click.click(); #click it
        button2click.click(); #click it again
        actions = ActionChains(driver); #fire up the actions
        actions.send_keys(medcond).perform(); #write in the medcond
        buttonSize = button2click.size;
        actions = ActionChains(driver); #fire up the actions
        actions.move_to_element_with_offset(button2click, buttonSize['width']//2, 3*buttonSize['height']//2);
        actions.click();
        actions.perform();
        
        #--- Move on to next ---
        button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")[0]; #search for elements with this string
        try:
            button2click.click(); #click it
        except:
            time.sleep(0.05); #give the page a chance to do stuff
            button2click.click(); #click it again idk it works prob off screen?
        #END TRY
        # time.sleep(0.1); #give the page a chance to do stuff
        
        # element = button2click
        # driverEle = element._parent
        # def apply_style(s):
        #     driverEle.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)
        # original_style = element.get_attribute('style')
        # apply_style("background: yellow; border: 2px solid red;")
        # #apply_style(original_style); #return to orig
        
        WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Great news')]")));     
        button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Great news')]"); #search for elements with this string
        if( len(button2click) > 0 ):
            button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Continue')]")[-1]; #search for elements with this string
            time.sleep(0.1); #give the page a chance to do stuff
            button2click.click(); #click it
            
            try:
                WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Immunization Scheduler')]")));
                
                
                button2click_text = driver.find_elements_by_xpath("//*[contains(text(), 'Results: ')]")[1].text; #search for elements with this string\
                try:
                    numStores = int(button2click_text[9:strstr(button2click_text,' stores').item()]);
                except:
                    numStores = 10; #assume 10 cause idk that Results: # stores thing doesn't always show apparently
                #END TRY
                
                for i in range(0,numStores):
                    button2click = driver.find_elements_by_xpath("//*[contains(text(), 'SELECT THIS STORE')]")[i+1];
                    try:
                        button2click.click(); #click it
                    except:
                        time.sleep(0.05); #give the page a chance to do stuff
                        button2click.click(); #click it again idk it works prob off screen?
                    #END TRY
                    button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")[0]; #search for elements with this string
                    try:
                        button2click.click(); #click it
                    except:
                        time.sleep(0.05); #give the page a chance to do stuff
                        button2click.click(); #click it again idk it works prob off screen?
                    #END TRY
                    time.sleep(0.5); #give the page a chance to do stuff
                    if( len(driver.find_elements_by_xpath("//*[contains(text(), 'check again another day')]")) <= 1 ): #Time of Day
                        riteaidWords.append(str(i+1)); #record the number that didn't tell you to check agian another day
                        riteaidSet['all reserved'] = False; #all reserved stays true, no appointments
                    else:
                        #catch a weird error
                        if( len(driver.find_elements_by_xpath("//*[contains(text(), 'Make an Appointment at Rite Aid')]")) > 0 ):
                            try:
                                driver.execute_script("window.onbeforeunload = function() {};")
                                driver.refresh(); #basically Next can move you forward but there's no avail (says so, using the calendar breaks it) so this gets out of it
                                driver.switch_to.alert.accept(); #i hope this works, the error on the website stopped happening
                                driver.switch_to.alert.accept(); #i hope this works, the error on the website stopped happening
                            except:
                                alert = driver.switch_to.alert;
                                alert.accept();
                                button2click = driver.find_elements_by_xpath("//*[contains(text(), 'Reload')]")
                                button2click.click(); #click it
                            #END TRY
                            WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Immunization Scheduler')]")));
                        #END IF                        
                    #END IF
                #END FOR i
            except TimeoutException:
                riteaidSet['all reserved'] = True; #all reserved stays true, no appointments
                driver.save_screenshot('riteaidWebsiteBroken.png'); #save a pic to check later
        else:
           riteaidSet['all reserved'] = True; #all reserved stays true, no appointments
       #END IF
    except:
        riteaidSet['all reserved'] = True; #all reserved stays true, no appointments
        driver.save_screenshot('riteaidNotSeenBefore.png'); #save a pic to check later
    #END TRY
    driver.save_screenshot('riteaidTest.png'); #save a pic to check later
    # try:
    #     myElem = WebDriverWait(driver, driverDelay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'are reserved at this time')]")));
    #     riteaidSet['all reserved'] = True; #all reserved stays true, no appointments
    # except TimeoutException:
    #     riteaidSet['all reserved'] = True; #all reserved stays true, no appointments
    #     driver.save_screenshot('riteaidNotSeenBefore.png'); #save a pic to check later
    # #END TRY
    driver.quit()
    # riteaidReturns = driver.find_elements_by_xpath("//*[contains(text(), 'are reserved at this time')]"); #search for elements with this string
    
    if( (riteaidSet['all reserved'] == False) ):
        #time to send email if either pass this
        subject = 'Riteaid Site Active'; #subject line
        message = 'Body: Riteaid at zipcode '+zipper+' has availability at store numbers '+' & '.join(riteaidWords)+' Site: '+riteaidCheck; #message body
        
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
        
        with open('timez_riteaid.pkl', 'wb') as filez:
            pickle.dump(currentTime, filez); #record the time sent
        #END WITH
    #END IF
    
    
    # if( riteaidReturn != riteaidOld ): #reduce overwrite of same thing
    #     with open(riteaidFile, 'w') as riteaider:
    #         riteaider.write(riteaidReturn); #write in the source code of the webpage
    #     #END WITH
    # #END IF
#END IF




























