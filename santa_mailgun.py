from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import random
import copy
import requests
import os
import sys

# handle input of the Mailgun API Token and Custom domain name
api_token = os.environ['API_TOKEN']
domain = os.environ["domain"]

if api_token == None:
    api_token = sys.argv[0]

if api_token == None:
    api_token = input("please enter in your mailgun API token")

if domain == None:
    domain = sys.argv[1]

if domain == None:
    domain = input("please enter in your domain name ex. the-north-pole.lol")

# checks that a pairing isn't the person with themself
# and that they aren't in the exclude (so couples don't get each other)
def isValid(pairings):
    for pair in pairings:
        if pair[0] == pair[1]:
            return False
        elif (pair[1]['name'] in pair[0]['exclude']):
            return False
    return True

# processes input data
def readInParticipants():
  with open('participants.json','r') as participants:
    data = (json.load(participants))
    return data
  
# mostly for debugging and seeing who has who
def listPairings(pairings):
    for gifter,giftee in pairings:
        print(f"{gifter['name']} will get a gift for {giftee['name']}" )

# shuffle the list so each gifter has a giftee
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

def email_handling(pair):

    gifter = pair[0]
    giftee = pair[1]
    
    # the message we want to send in the body
    html = f"""
    <html>
    <head></head>
    <body>
        <h1>Merry Christmas %s!</h1>
        This year, your secret santa is %s!
        </p>
    </body>
    </html> """ % (gifter['name'],giftee['name'])

    # api endpoint for mailgun
    endpoint = f"https://api.mailgun.net/v3/{domain}/messages"
    
    data={
        "from": "Santa santa@the-north-pole.lol",
        "to": [f"{gifter['name']}",f"{gifter['email']}"],
        "subject": "Your Secret Santa",
        "html": f"{html}"}
    
    requests.post(endpoint,auth=("api", api_token),data=data)


def main():
    json_data = readInParticipants()
    pairings = generateList(json_data)
    valid = isValid(pairings)
    # keeps trying pairings
    # since the problem space is small we can do this
    while valid == False:
        pairings = generateList(json_data)
        valid = isValid(pairings)
    listPairings(pairings)

    for pair in pairings:
        email_handling(pair)
    print("emails sent!!")
    



main()


