import time
from enum import Enum
from http import HTTPStatus

import requests
from requests.exceptions import HTTPError

RETRY_CODES = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]


class RequestFailed(Exception):
    pass


class RequestType(Enum):
    POST = 1
    GET = 2


def make_request(url, req_type=RequestType.GET, params=None, retries=3):
    '''
    Function for making a request to a given url. Passes along the given parameters

    :param url:
    :param req_type:
    :param params:
    :param retries:
    :return: Returns the JSON response from the url, or raises an exception
    '''

    for _ in range(retries):
        try:
            response = requests.get(url, params) if req_type == RequestType.GET else requests.post(url, params)
            response.raise_for_status()

            try:
                return response.json()
            except:
                raise RequestFailed

        except HTTPError as exc:
            code = exc.response.status_code

            if code in RETRY_CODES:
                time.sleep(1)
                continue

            raise RequestFailed

