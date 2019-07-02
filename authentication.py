
# Authentication.py
# Purpose: Parse API keys from charity.auth file.

import glob
import sys

authentication_files = glob.glob('./*.auth')

def exitWithMessage(message):
    print (message)
    sys.exit(1)

try:
    assert len(authentication_files) == 1
except AssertionError:
    if (len(authentication_files) == 1):
        exitWithMessage("You must create one .auth file with your Twitter credentials!")
    else:
        exitWithMessage("You cannot have more than one .auth file with your Twitter credentials!")

consumer_key = ""
consumer_secret = ""
access_token = ""
token_secret = ""

with open(authentication_files[0]) as file:
    for line in file:
        split_line = line.split(":")
        if (split_line[0] == "consumer_key") :
            consumer_key = split_line[1].strip()
        elif (split_line[0] == "consumer_secret"):
            consumer_secret = split_line[1].strip()
        elif (split_line[0] == "access_token"):
            access_token = split_line[1].strip()
        elif (split_line[0] == "token_secret"):
            token_secret = split_line[1].strip()
        else:
            exitWithMessage("The key " + split_line[0].strip() + " is not recognized!")

if not consumer_key:
    exitWithMessage("Your .auth file must contain a key for consumer_key.")
if not consumer_secret:
    exitWithMessage("Your .auth file must contain a key for consumer_secret.")
if not access_token:
    exitWithMessage("Your .auth file must contain a key for access_token.")
if not token_secret:
    exitWithMessage("Your .auth file must contain a key for token_secret.")
