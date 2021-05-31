from urllib import request
import json


def send_message_to_slack_by_hook(text, webhook):
    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request(webhook,
                              data=json_data.encode('utf-8'),
                              headers={'Content-Type': 'application/json'})
        request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))
