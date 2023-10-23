#!/usr/local/bin/python3

import requests
import sys
import json
import os 
import subprocess
from dotenv import load_dotenv

load_dotenv()
#####
def format_json(data):
    data = json.load(data)
    questions_and_answers = []

    for _, question_data in data["Survey_Name"]["Page_Name"].items():
        question = {
            "description": question_data["Description"],
            "answers": question_data["Answers"]
        }
        questions_and_answers.append(question)

    start= '''
    {
    "title": "crazy cool survey",
    "pages": [
        {
            "title": "choose carefully",
            "questions": [
    '''
    ending = '''
                ]
            }     
        ]
    }
    '''

    for question in questions_and_answers:
        start+='''
                {
            "headings": [
                {
                    "heading":"'''+question["description"] +''' "
                }
            ],
            "position": 1,
            "family": "single_choice",
            "subtype": "vertical",
            "answers": {
                "choices":['''
        
        for answer in question["answers"]:
            start+='''
                {
                    "text":"'''+ answer +''' "
                },'''
        start = start[:-1]

        start+='''
                ],
                "other":[
                        {
                            "text": "Other",
                            "num_chars": 100,
                            "num_lines": 3
                        }
                ]
            }
        },'''
    
    start=start[:-1]

    start+=ending
    #print(start)
    return start
    #print(questions_and_answers)


def create_survey(api_key, survey_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    api_url = 'https://api.surveymonkey.com/v3/surveys'

    response = requests.post(api_url, headers=headers, json=survey_data)

    if response.status_code == 201:
        print("Survey created successfully!")
        return response.json()['id']
    else:
        print(f"Failed to create survey. Status code: {response.status_code}")
        print(response.text)
        return None

def send_invitations(api_key, survey_id, recipients):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    api_url = f'https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors'

    collector_data = {
        "type": "weblink",
        "name": "crazy cool collector"
    }

    response = requests.post(api_url, headers=headers, json=collector_data)

    if response.status_code == 201:
        resjson = response.json()
        #collector_id = resjson['id']
        print("Collector created successfully")
        weblink =resjson['url']
        print(weblink)

        recipients = json.dumps(recipients)
        output = subprocess.check_output(['./sendmail.py', weblink, recipients],text=True)
        print(output)
        
        #email collectors are part of a premium plan on surveymonkey :( )
        # add recipients to the collector
        #recipient_api_url = f'https://api.surveymonkey.com/v3/collectors/{collector_id}/recipients'
        #recipient_data = {
        #    "contacts": [{"email": recipient} for recipient in recipients]
        #}

        #recipient_response = requests.post(recipient_api_url, headers=headers, json=recipient_data)

        #if recipient_response.status_code == 201:
        #    print("Recipients added successfully!")
        #else:
        #    print(f"Failed to add recipients. Status code: {recipient_response.status_code}")
        #    print(recipient_response.text)
    else:
        print(f"Failed to create collector. Status code: {response.status_code}")
        print(response.text)

api_key = os.getenv("SMAPI")


with open(sys.argv[1], 'r') as data:
    formatted_data= format_json(data)
    survey_data = json.loads(formatted_data)

input_string = input("Enter email addresses separated by commas: ")

email_addresses = [email.strip() for email in input_string.split(',')]

recipients = [{"email": email} for email in email_addresses]

print("Loaded recipients")

survey_id = create_survey(api_key, survey_data)

if survey_id:
    send_invitations(api_key, survey_id, recipients)

