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
    return cookie_dictionary

# send a post request with auth cookies to claim materials, primos, and food from hoyo website
def claim_rewards(cookie_dictionary):
    url = "https://hk4e-api-os.mihoyo.com/event/sol/sign?act_id=e202102251931481&lang=en-us"

    try:
        ltuid = cookie_dictionary["ltuid"]
        # sometimes ltuid is missing from cookie storage, use account_id as a backup
        if ltuid == None:
            ltuid = cookie_dictionary["account_id"]
        ltoken = cookie_dictionary["ltoken"]
        cookies = {'ltuid': ltuid, 'ltoken': ltoken}

        r = requests.post(url, cookies=cookies)
        # print status of request
        res = r.json()
        print(res)
        if res['retcode'] == -100:
            raise Exception("claim failed")
    except KeyError as e:
        print("Key " + e.args[0] + " is missing from cookie storage.") 
        print("Verify that either your repo secrets are correct or you are logged in correctly with your browser.")
        print("Exiting.")
        exit()


data = open_json_file('config.json')
rewards_options = data.get("rewards_options")
print("Rewards opts: ")
print(rewards_options)

cookie_dictionary = {}
if is_workflow_enabled(rewards_options):
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