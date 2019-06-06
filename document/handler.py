import json
from urllib import request, error, parse


def get_page_title_handler(event, context):

    failure = None
    page_title = "NO TITLE"
    url = event['page_url']
    try:
        webpage = request.urlopen(url).read()
        try:
            page_title = str(webpage).split('<title>')[1].split('</title>')[0]
        except Exception as e:
            failure = str(e)
    except Exception as e:
        failure = str(e)

    body = {
        "page_title": page_title,
        "failure": failure
    }

    statusCode = 400 if failure else 200
        
    response = {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

    return response
