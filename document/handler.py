from urllib import request
from bs4 import BeautifulSoup as bs

from helpers import (
    store_response_to_s3,
    save_to_db,
    build_response,
    id_generator
)

s3_bucket_url = None


def get_page_title_handler(event, context):

    failure = None
    page_title = "NO TITLE"
    global s3_bucket_url
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
    if not failure:
        s3_bucket_url = store_response_to_s3(webpage)
        save_to_db(page_title)

    s3_bucket_url = s3_bucket_url if s3_bucket_url else None
    return build_response(failure, page_title, s3_bucket_url)
