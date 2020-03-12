import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import praw

def main():
    reddit = praw.Reddit(client_id='<INESRT REDDIT CLIENT ID HERE>',
                         client_secret='<INSERT REDDIT CLIENT SECRET HERE>',
                         username='<INSERT USERNAME OF REDDIT BOT HERE>',
                         password='<INSERT REDDIT PASSWORD HERE>',
                         user_agent='ModBot')

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('<INSERT THE FILE NAME FOR YOU GOOGLE API CREDENTIALS HERE>', scope)
    
    client = gspread.authorize(creds)

    sheet = client.open('<INSERT NAME OF SPREADSHEET ON YOUR GOOGLE DRIVE HERE>').sheet1

    lagtime = 2 # This is used to make sure read/write tokens gsheets aren't exhausted. Lower this number at your own risk,
    # but you might be able to get away with it if you apply for more read/write tokens per 100 seconds
    # through google docs.
    
    crawlreddit = reddit.subreddit('<INSERT SUBREDDIT TO BE MODERATED HERE>')  # subreddit to be moderated


    while True: 
        print('Initiating....')
        try:
            start_time = 0
            for log in reddit.subreddit('fffffffuuuuuuuuuuuu').mod.log(limit=10000):
                userExists = True

                if log.action == 'removelink':
                    try:
                        str = "https://old.reddit.com/" + log.target_permalink
                        Submission = reddit.submission(url=str)
                        print('link url:' + Submission.url)
                        print('link author:' + Submission.author.name)
                    except Exception as u:
                        print('User deleted account!')
                        print('=====================')
                        userExists = False

                    if userExists:
                        try: #If the user is already registered, increment their row. If not, create a new row
                            cell = sheet.find(Submission.author.name)
                            colNumber = cell.col
                            rowNumber = cell.row
                            value = sheet.cell(rowNumber, (colNumber + 1)).value
                            if value == '':
                                value = 0
                            totalRemoved = int(value)
                            totalRemoved += 1
                            sheet.update_cell(rowNumber, (colNumber + 1), totalRemoved)
                            time.sleep(lagtime)
                        except Exception as u:
                            print('new user!')
                            value = sheet.acell('Z1').value # Total number of usernames will be stored in Z1
                            totalUsernames = int(value)
                            totalUsernames += 1
                            sheet.update_acell('Z1' , totalUsernames)
                            sheet.update_cell((totalUsernames + 1), 1, Submission.author.name)
                            sheet.update_cell((totalUsernames + 1), 2, 1)  # The first infringement is always 1
                            time.sleep(lagtime)

                if log.action == 'removecomment':
                    try:
                        str = "https://old.reddit.com/" + log.target_permalink
                        Comment = reddit.comment(url=str)
                        print('comment body:' + log.target_body)
                        print('comment author:' + Comment.author.name)
                    except Exception as u:
                        print('User deleted account!')
                        print('=====================')
                        userExists = False

                    if userExists:
                        try: #If the user is already registered, increment their row. If not, create a new row
                            cell = sheet.find(Comment.author.name)
                            colNumber = cell.col
                            rowNumber = cell.row
                            value = sheet.cell(rowNumber, (colNumber + 2)).value
                            if value == '':
                                value = 0
                            totalRemoved = int(value)
                            totalRemoved += 1
                            sheet.update_cell(rowNumber, (colNumber + 2), totalRemoved)
                            time.sleep(lagtime)
                        except Exception as u:
                            print('new user!')
                            value = sheet.acell('Z1').value # Total number of usernames will be stored in Z1
                            totalUsernames = int(value)
                            totalUsernames += 1
                            sheet.update_acell('Z1' , totalUsernames)
                            sheet.update_cell((totalUsernames + 1), 1, Comment.author.name)
                            sheet.update_cell((totalUsernames + 1), 3, 1)  # The first infringement is always
                            time.sleep(lagtime)

            break
        except Exception as e:
            traceback.print_exc()  # Should only be happen when reddit servers stutter


if __name__ == "__main__":
    main()
