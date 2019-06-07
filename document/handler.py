from urllib import request
from bs4 import BeautifulSoup as bs

from helpers import (
    store_response_to_s3,
    save_to_db,
    build_response,
    id_generator,
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
    url_uuid = event['url_uuid']
    url = get_url_from_uuid(url_uuid)
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
    if not failure:
        s3_bucket_url = store_response_to_s3(webpage)
        update_record(s3_bucket_url, page_title, url_uuid)
        update_record_processed(url_uuid)
    else:
        raise Exception(failure)


def create_request_identifier_handler(event, context):
    url = event['page_url']
    url_uuid = generate_identifier(url)
    save_to_record(url, url_uuid)
    data = {
        "url_uuid": url_uuid
    }
    invoke_processing_lambda(data)

    return url_uuid
