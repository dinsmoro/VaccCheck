# VaccCheck
Emails or texts (through email-to-sms) when vaccine availabilities open up for your particular state (state &amp; supported stores must intersect for anything to be found though).

# Supported Sites:
Weis

Wegmans

# How it works:
Code checks for vaccine availability for supported sites. For all current supported sites it checks using an automated Chrome browser since those sites have chatbots that I could only figure out how to navigate with a real browser.

If there is availability in your state, it will email/text-through-email whatever destinations you set.

There is a time limit (user definable) between alerts, so it doesn't spam you.

The code will save a picture of what it thinks are successful vaccine openings and not-before-seen stuff. That save code can be commented out, it's just for feedback.

I would reccomend that you make a new email to send from if you want to be extra secure, as you have to hardcode your email's password into the deltaWeb_xxx.py scripts for them to send emails from your email address.

# Limits:
- It will spam you if there are vaccine appointments in a far-off area of your state that are available. Sub-state areas could be added but I don't know what they are so I haven't added support for that. It would be another nested try and WebDriverWait call for the sub-state string if the sub-state strings were known.
- The web parsing takes like a minute due to waiting up to 15 sec (user configurable) for each element to load. That limits how often you can check, basically.

# Requirements:
- Tested on Windows. Theoretically it can work on any OS, in practice I'm not sure since there's integration with Chrome and path stuff for the time file.
- Python 3+
- Chrome Web Driver https://chromedriver.chromium.org/downloads
- A computer that is always on, so it can always check

# How to use it:
- Download and install Chrome
- Download Chrome Web Driver, put it somewhere and add that folder to your path (in Windows search "edit the system environment variables", choose the suggestion for System Properties -> click on the Environment Variables button -> under User variables for {USER} click on Path to highlight it -> click on the Edit... button under that box -> Click on the New button -> Type the path of the folder with the Chrome Web Driver into that path. "OK" out of all of those windows.
- Download Anaconda https://www.anaconda.com/products/individual it comes with most packages needed, set in path if you are the only user of the computer because it'll make calling pythonw.exe easier
- Open Anaconda Prompt (now in your start menu) and type "conda install selenium" to get selenium because it didn't come with the default packages
- Set the deltaWeb_xxx.py you want to check regularly to be run on a schedule in your OS's method to run scheduled tasks. In Windows, open Task Scheduler -> Create Task... -> Triggers tab -> New Trigger -> One Time -> Repeat task every: 5 minutes (safe since takes a minute or so to complete a worst-case check) -> for  a duration of: Indefinitely -> OK -> Actions tab-> New... -> Start a program (default) -> Program/script: C:\path\to\pythonw.exe (in the Anaconda install folder, in quotes if there are spaces in the address) -> Add agruments (optional): C:\path\to\deltaWeb_xxx.py (in quotes if there are spaces in the address) -> OK. -> OK. & done.
- You can test the code by calling it with python.exe from the Command Prompt, pythonw.exe is windowless and won't show you errors that occur (great for running on a schedule, not so much for debug).
- Open deltaWeb_xxx.py and enter the state abberviation you want for the stater variable, specify the resendLimit (60 to start), enter the email you will send from, enter the password for the email you will send from (I'm not sure how secure the email stuff is but it's a built-in Python library so I hope it is pretty safe) - you will probably need to make a legacy password for it since it can't do 2 factor stuff or anything like that, enter the email/email-to-text destinations you want (I'm not sure if there is a limit).
- Done, so simple to check for vaccines!
