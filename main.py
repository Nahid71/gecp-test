# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape
# [START functions_http_method]
# [START functions_helloworld_get]
import functions_framework

# [END functions_helloworld_http]
# [END functions_http_content]
# [END functions_http_method]
# [END functions_helloworld_get]


# [START functions_helloworld_get]
@functions_framework.http
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    return 'Hello World!'
# [END functions_helloworld_get]


# [START functions_helloworld_http]
@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))
# [END functions_helloworld_http]

# [START functions_http_content]
@functions_framework.http
def hello_content(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data
    elif content_type == 'text/plain':
        name = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello {}!'.format(escape(name))
# [END functions_http_content]


# [START functions_http_method]
@functions_framework.http
def hello_method(request):
    """ Responds to a GET request with "Hello world!". Forbids a PUT request.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    from flask import abort

    if request.method == 'GET':
        return 'Hello World!'
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)
# [END functions_http_method]


# [START functions_helloworld_error]
@functions_framework.http
def hello_error_1(request):
    # This WILL be reported to Error Reporting,
    # and WILL NOT show up in logs or
    # terminate the function.
    from google.cloud import error_reporting
    client = error_reporting.Client()

    try:
        raise RuntimeError('I failed you')
    except RuntimeError:
        client.report_exception()

    # This WILL be reported to Error Reporting,
    # and WILL terminate the function
    raise RuntimeError('I failed you')
# [END functions_helloworld_error]


# [START functions_helloworld_error]
@functions_framework.http
def hello_error_2(request):
    # These errors WILL NOT be reported to Error
    # Reporting, but will show up in logs.
    import logging
    import sys
    print(RuntimeError('I failed you (print to stdout)'))
    logging.warn(RuntimeError('I failed you (logging.warn)'))
    logging.error(RuntimeError('I failed you (logging.error)'))
    sys.stderr.write('I failed you (sys.stderr.write)\n')

    # This is considered a successful execution and WILL NOT be reported
    # to Error Reporting, but the status code (500) WILL be logged.
    from flask import abort
    return abort(500)
# [END functions_helloworld_error]