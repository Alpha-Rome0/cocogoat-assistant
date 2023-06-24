import browser_cookie3
import json
import os
import requests

# opens and returns data from json file, else exits
def open_json_file(f):
    try:
        with open(f, "r") as jsonfile:
            data = json.load(jsonfile)
            print("Read of " + f + " successful!")
            return data
    except FileNotFoundError:
        print("Sorry, the file " + f + " does not exist. Exiting.")
        exit()

# check to see if a string is valid json (true), else throws ValueError and returns false
def is_json(j):
    try:
        json.loads(j)
    except ValueError as e:
        return False
    return True

# configure script based on local or workflow option
def is_workflow_enabled(options):
    if options.get("use_workflow") == "true":
        return True
    # workflow is either disabled or missing
    return False

# select browser based on config file options
# locate hoyo cookies and return them
def get_local_cookies(browser_choice):
    print("Browser chosen is: " + browser_choice)
    # call different module functions based on browser, ex: browser_cookie3.firefox()
    # using browser as a variable string
    get_cookies_from_selected_browser = getattr(browser_cookie3, browser_choice)

    # only select cookies for hoyolab.com domain, store in cookie jar
    jar = get_cookies_from_selected_browser(domain_name='hoyolab.com')
    cookie_dictionary = requests.utils.dict_from_cookiejar(jar)

    return cookie_dictionary

# get hoyo cookies using github workflow with repo secrets
def get_workflow_cookies():
    cookie_dictionary = {}

    cookie_dictionary['ltuid'] = os.environ.get('LTUID')
    cookie_dictionary['ltoken'] = os.environ.get('LTOKEN')
    cookie_dictionary['accountid'] = 'e202102251931481'
    return cookie_dictionary

def check_response(response):
    if is_json(response):
        parsed_response = response.json()
        print(parsed_response)
        if parsed_response['retcode'] == -100:
            raise Exception("Rewards claim failed!")
    else:
        print("Response not empty but it's not valid json!")
        print("Response was:")
        print(response)
        print("Exiting.")
        exit()
    return

# send a post request with auth cookies to claim materials, primos, and food from hoyo website
def claim_rewards(cookie_dictionary):
    # add headers to format post request properly
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://webstatic-sea.mihoyo.com',
        'Connection': 'keep-alive',
        'Referer': f'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481',
    }

    params = (
        ('lang', 'en-us'),
    )

    data = {'act_id': cookie_dictionary["accountid"]}
    # this is the url for sending the post request, can also get claim status by sending a get request
    url = "https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us"

    try:
        ltuid = cookie_dictionary["ltuid"]
        # sometimes ltuid is missing from cookie storage, use accountid as a backup
        if ltuid == None:
            print("ltuid not found, using accountid instead.")
            ltuid = cookie_dictionary["accountid"]
        ltoken = cookie_dictionary["ltoken"]
        cookies = {'ltuid': ltuid, 'ltoken': ltoken}

        r = requests.post(url, headers=headers, params=params, cookies=cookies, json=data)
        # print status of request

        if r is not None:
            if r.status_code is not None: print(r.status_code)
            print(r.text)
            check_response(r.text)
        else:
            print("An empty response body was returned!")
    except KeyError as e:
        print("Key " + e.args[0] + " is missing from cookie storage.")
        print("Verify that either your repo secrets are correct or you are logged in correctly with your browser.")
        print("Exiting.")
        exit()


data = open_json_file('config.json')
rewards_options = data.get("rewards_options")
print("Rewards options selected: ")
print(rewards_options)

cookie_dictionary = {}
if is_workflow_enabled(rewards_options):
    print("Using GitHub action workflow to claim rewards.")
    cookie_dictionary = get_workflow_cookies()
else:
    if rewards_options.get("browser") is not None:
        browser_choice = rewards_options["browser"].lower()
        print(browser_choice)
        browsers_supported = {"chrome", "firefox", "opera", "edge", "chromium", "brave", "vivaldi"}

        if browser_choice not in browsers_supported:
            print("Browser choice " + browser_choice + " is not supported at this time.")
            exit()
        cookie_dictionary = get_local_cookies(browser_choice)
        print(cookie_dictionary)
    else:
        print("Browser is missing from config.json file! Exiting.")
        exit()

claim_rewards(cookie_dictionary)