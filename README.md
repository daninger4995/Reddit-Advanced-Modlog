# Reddit-Advanced-Modlog
Creates a repository summarizing disciplanary actions taken by user.

The bot will skim the modlog of a subreddit, and record every time an action is taken against a user.
This will enable moderators of subreddits to more easily keep track of how many rule violations 
specific users have commit. All of this information will be dumped to a Google Sheet, which can
then be shared with other mods or even made public.

PREREQUISITES:

pip install praw gspread google-api-python-client google-auth google-auth-httplib2 oauth2client

Make sure you are running python3.8

Create a reddit account created specifically for this bot, and go to preferences > apps, and create
an app for this bot as a "personal script". Take the client id, client secret, account username, 
and account password, and add it to the .py file in the specified location. Then, make sure to add 
the bot account as a mod to the subreddit you wish to create a database for; this bot functions off 
examining the modlog which only mods have access to.

Next, go to this link: https://console.developers.google.com/apis/library

Agree to Google's TOS, and then create a project with an apropriate title. Then, within
the library, add Google Drive and Google Sheets APIs to the project's library. Now, create your
credentials for the project, giving it access to application data. When creating the service account,
grant the account the role of "editor". You will then be able to download a JSON file, put this in
the path wherever you are running the .py file from. Make sure to enter the name of this file into
the script in the specified location. 

Now, create a google sheet from your account, entering the name of this sheet into the script in the
specified location. Within the JSON file downloaded earlier, there will be a line that reads,
"client_email". Copy this email address, and share the google doc with this email address.

USEFUL VIDEO FOR AID IN SETTING UP GOOGLE SHEETS API: https://www.youtube.com/watch?v=vISRn5qFrkM

Finally, make sure to enter "0" into cell "Z1" of the spreadsheet, and format the cell as a number. 
This is used to index how long the list is without exhausting reaed/write tokens from google's API.

If you intend to run this script once to create a database of the past 30 days, then run 
just run Modlog_initial.py. If would rather have this google sheet update constantly, than run
Modlog_Live.py. You could also run Modlog_initial.py once, and then have Modlog_live.py running
constantly to immediatley build up a database and have it constantly being updated.

