import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import random
import copy
import getpass

gmail_address = input("please put in your SMTP username ")
gmail_password = getpass.getpass("please provide your SMTP password: ")

# checks that no one is paired with themselves
# and that no one has someone in their exclude lists 
def isValid(pairings):
    for pair in pairings:
        if pair[0] == pair[1]:
            return False
        elif (pair[1]['name'] in pair[0]['exclude']):
            return False
    return True

def generateList(user_list):

    pairings = []
    
    # making copies of the people in secret santa
    gifter_list = copy.deepcopy(user_list)
    giftee_list = copy.deepcopy(user_list)

    #shuffle em up
    random.shuffle(gifter_list)
    random.shuffle(giftee_list)
    
    # Keep popping off pairs until we get good matches
    while(len(giftee_list) > 0):
        gifter = gifter_list.pop()
        giftee = giftee_list.pop()
            
        pairings.append([gifter,giftee])
    # return our pairs of gifters and giftees
    return pairings            


# processes input data
def readInParticipants():
  with open('participants.json','r') as participants:
    data = (json.load(participants))
    return data
    
# mostly for debugging and seeing who's who
def listPairings(pairings):
    for gifter,giftee in pairings:
        print(f"{gifter['name']} will get a gift for {giftee['name']}" )

def email_handling(pair):

    gifter = pair[0]
    giftee = pair[1]
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    # Authentication
    s.login(gmail_address, gmail_password)
    
    
    # message to be sent 
    msg = MIMEMultipart('alternative')

    html = f"""
    <html>
    <head></head>
    <body>
        <h1>Merry Christmas %s!</h1>
        This year, your secret santa is %s!
        </p>
    </body>
    </html>""" % (giftee['name'],gifter['name'])


    part2 = MIMEText(html, 'html')
    msg['Subject'] = "Your Secret Santa"
    msg.attach(part2)
    # sending the mail
    s.sendmail(gmail_address, giftee['email'], msg.as_string())

    # terminating the session
    s.quit()


def main():
    json_data = readInParticipants()
    pairings = generateList(json_data)
    
    valid = isValid(pairings)
    while valid == False:
        pairings = generateList(json_data)
        
        valid = isValid(pairings)
    listPairings(pairings)
    
    for pair in pairings:
        email_handling(pair)
    print("emails sent!!")
    

main()
