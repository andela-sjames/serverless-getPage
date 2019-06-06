import json
import random
import string
from urllib import request, error, parse

import boto3
from bs4 import BeautifulSoup as bs

# connect to s3
s3 = boto3.client('s3')

# connect to dynamodb
db_table = boto3.resource('dynamodb').Table('UrlDocument')


def get_page_title_handler(event, context):

    failure = None
    page_title = "NO TITLE"
    url = event['page_url']
    try:
        response = request.urlopen(url)
        webpage = bs(response, features="html.parser")
        try:
            page_title = webpage.title.string
        except Exception as e:
            failure = str(e)
    except Exception as e:
        failure = str(e)

    # get the webpage and store to s3
    if failure is not None:
       s3_bucket_url = store_response_to_s3(webpage)
       save_to_db(page_title)

    return build_response(failure, page_title, s3_obj_url)

def store_response_to_s3(webpage):
    page_body = webpage.content
    s3_bucket = 'url-bucket-1047'
    s3_key = f'pages/{id_generator()}'
    s3.put_object(
        ACL='public-read',
        Body=page_body,
        Bucket=s3_bucket,
        Key=s3_key
    )

    # get s3 object url using virtual hosted style
    s3_bucket_url = f'https://{s3_bucket}.s3.amazonaws.com/{s3_key}'
    return s3_bucket_url

def save_to_db(title):
    response = db_table.put_item(
        Item={
            'title': title,
        }
    )

def build_response(failure, page_title, s3_bucket_url=None):
    
    body = {
        "page_title": page_title,
        "s3_bucket_url": s3_bucket_url,
        "failure": failure
    }

    statusCode = 400 if failure else 200
    response = {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

    return response

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
