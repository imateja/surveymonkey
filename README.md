# Survey and Collector creation using Survey Monkey API
This is a python script that creates a survey, then creates a weblink collector for it and after sends emails containing the weblink to email addresses of your choosing

## Usage

```sh
pip install dotenv
./surveys.py questiondata.json
```
``` surveys.py``` is the main script that creates a survey and calls the script to send emails
``` sendmail.py``` is a script that is called and sends emails to recipients

First the JSON is formatted because the input isn't what SurveyMonkey API expects.
After that we create the survey by using the ```requests``` library to send a POST request.
If the survey creation was successful, we create a weblink collector (since that's the only collector that doesn't require a premium plan on the website)
Then we call another script to send the emails by using the ```subprocess``` library.

