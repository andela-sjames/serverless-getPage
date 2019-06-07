from urllib import request
from bs4 import BeautifulSoup as bs

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from helpers import (
    store_response_to_s3,
    generate_identifier,
    save_to_record,
    invoke_processing_lambda,
    get_url_from_uuid,
    update_record,
    update_record_processed
)

s3_bucket_url = None


def get_page_title_handler(event, context):

    failure = None
    page_title = "NO TITLE"
    global s3_bucket_url

    records = event['Records']

    # log to cloudwatch
    logger.info(records)

    for record in records:
        if record['eventName'].upper() in {'INSERT', 'MODIFY'}:

            # primary key
            record_id = record['dynamodb']['Keys']['uuid']['S']

            # init local vars
            new_url = None
            new_image = record['dynamodb'].get('NewImage') or {}

            # new values
            if 'url' in new_image:
                new_url = new_image['url']['S']

        try:
            response = request.urlopen(new_url)
            webpage = bs(response, features="html.parser")
            try:
                page_title = webpage.title.string
            except Exception as e:
                failure = str(e)
        except Exception as e:
            failure = str(e)

        # get the webpage and store to s3
        if not failure:
            s3_bucket_url = store_response_to_s3(webpage)
            update_record(s3_bucket_url, page_title, record_id)
            update_record_processed(record_id)
        else:
            raise Exception(failure)


def create_request_identifier_handler(event, context):
    url = event['page_url']
    url_uuid = generate_identifier(url)
    save_to_record(url, url_uuid)

    return url_uuid
