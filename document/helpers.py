"""Helper script defined for lambda function."""
import json
import random
import string
import uuid

import boto3

# connect to s3
s3 = boto3.client('s3')

# connect to dynamodb
dynamodb = boto3.client('dynamodb')

# connect to lambda
invokeLambda = boto3.client('lambda', region_name='us-east-1')


def store_response_to_s3(webpage):
    page_body = webpage.encode()
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
    dynamodb.put_item(
        TableName='UrlDocument',
        Item={
            'title': {'S': title}
        }
    )


def build_response(failure, page_title, s3_bucket_url):
    
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


# generate a UUID based on MD5 hash with a URL string
def generate_identifier(page_url):
    return uuid.uuid3(uuid.NAMESPACE_URL, page_url)


def send_data_to_db(url, url_uuid):
    dynamodb.put_item(
        TableName='UrlDocument',
        Item={
            'uuid': {'S': url_uuid}
            'url': {'S': url}
            'state': {'S': 'PENDING'}
        }
    )

# invoke your lambda function from another lambda function.
def invoke_processing_lambda(data):
    invokeLambda.invoke(FunctionName = 'getPageTitle', InvocationType = 'Event', Payload = json.dumps(data))

