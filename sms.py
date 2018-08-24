import subprocess
import requests
#curl -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' --header 'Authorization: testmessage' --header 'Accept-Language: en-US' -d '{ \ 
#   "message": { \ 
#     "alert": "Notification alert message" \ 
#   } \ 
# }' 'https://imfpush.ng.bluemix.net/imfpush/v1/apps/ad12214a-6184-4cbb-aa79-606faca12514/messages'

SMS_URL = "https://imfpush.ng.bluemix.net/imfpush/v1/apps/ad12214a-6184-4cbb-aa79-606faca12514/messages"

def send_sms(number,message):
    payload = {'message':{'alert':number +',' + message}}
    headers = {'Accept-Language':'en-US'}
    headers['Authorization'] = get_token() 
    response= requests.post(SMS_URL, json = payload, headers=headers)
    print(response.text)
    print(response.status_code)


def get_token():
    result = subprocess.run(['ibmcloud', 'iam', 'oauth-tokens'], stdout=subprocess.PIPE)
    #HACK: dont talk to me about bad code. i know. 
    raw_token = str(result.stdout).split('Bearer')[1].split('\\')[0].strip()
    return raw_token


#send_sms('9637895831','hello world')
