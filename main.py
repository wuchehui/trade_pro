# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, flash, redirect, render_template, request, url_for
from pprint import pprint as pp
from weather import query_api
from quote import query_stock
from quote import query_stock_urllib3

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    #return 'Hello World!'
    '''
    return render_template(
        'weather.html',
        data=[{'name':'Toronto'}, {'name':'Montreal'}, {'name':'Calgary'},
        {'name':'Ottawa'}, {'name':'Edmonton'}, {'name':'Mississauga'},
        {'name':'Winnipeg'}, {'name':'Vancouver'}, {'name':'Brampton'}, 
        {'name':'Quebec'}])
    '''
    return render_template(
        'weather.html',
        data=[{'name':'AMD'}, {'name':'BA'}, {'name':'CVX'},
        {'name':'DIS'}, {'name':'EBAY'}, {'name':'FB'},
        {'name':'GILD'}, {'name':'HD'}, {'name':'INTC'},
        {'name':'JPM'}])

@app.route("/result", methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('comp_select')
    #resp = query_api(select)
    resp = query_stock(select)
    #resp = query_stock_urllib3(select)
    #print(resp)
    pp(resp)
    if resp:
       data.append(resp)
    if len(data) != 2:
        error = 'Bad Response from Weather API'
    return render_template(
        'result.html',
        data=data,
        error=error)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
