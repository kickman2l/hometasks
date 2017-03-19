#!/usr/bin/python
# ------------------------------------------------ import block ------------------------------------------------------ #


import requests
import json
import argparse
import datetime
from datetime import date


# -------------------------------------------------- arguments block ------------------------------------------------- #

authen = ('kickman2l', '1780ad6879df1b3988127d94f7483f071d86f1be')

parser = argparse.ArgumentParser(usage='%(prog)s <user> <repository name> -num <req number> -o <opt1 opt2 opt3>',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("username", nargs='+', help="GitHub username")
parser.add_argument("repository", nargs='+', help="GitHub repository name")
parser.add_argument("-v", "--version", action='version', version='%(prog)s 0.001')
parser.add_argument("-oad", "--opened_after_date", type=str, metavar="",
                    help="Option to consider only pull requests opened on or after this date. Format 2017-03-14(Y-M-D)")
parser.add_argument("-ocd", "--opened_before_date", type=str, metavar="",
                    help="Only consider pull requests opened before this date. Format 2017-03-14(Y-M-D)")
parser.add_argument("-num", "--number", metavar="", help="Works with parameters for single request. More info -h.")
parser.add_argument("-o", "--options", nargs='*', metavar="", type=str, help="Possible additional options:\n"
    "bs  = Basic statistics about merged/closed rate.\n"
    "\nNext parameters will works only with parameter -num:\n"
    "ncc = Number of comments created.\n"
    "ndo = Number of days opened.\n"
    "dwo = Day of the week opened.\n"
    "dwc = Day of the week closed.\n"
    "wo  = Week opened.\n"
    "wc  = Week closed.\n"
    "uo  = User who opened.\n"
    "uc  = User who closed.\n"
    "al  = Attached labels.\n"
    "nla = Number of lines added.\n"
    "nld = Number of lines deleted.\n"
    "hdc = Hour of the day closed.\n"
    "hdo = Hour of the day opened.")
args = parser.parse_args()
# ------------------------------------- Functions for processing options --------------------------------------------- #


def summary_rep_inf(res):
    print("req.number  state  user          created                           title")
    for i in res:
        print(str(i["number"]) + "          " + str(i["state"]) + "   " + str(i["user"]["login"])
              + "        " + str(i["created_at"]) + "        " + str(i["title"]))


def summary_single_inf(res):
    print("req.number  state  user          created                           title")
    print(str(res["number"]) + "          " + str(res["state"]) + "   " + str(res["user"]["login"])
          + "        " + str(res["created_at"]) + "        " + str(res["title"]))


def bs(res):
    merged = 0
    closed = 0
    for i in res:
        if i["merged_at"]:
            merged += 1
        if i["closed_at"]:
            closed += 1
    print("Repository " + str(args.repository[0]) + ": merged requests=" + str(merged) + ". Closed requests="
          + str(closed)+".")


def oad(res, string_date):
    is_find_val = 0
    result = []
    data_array = []
    str_d = string_date.split("-")
    for val in str_d:
        result.append(int(val))
    for rec in res:
        if rec["state"] == "open":
            arr = []
            for val in rec["created_at"].split("T")[0].split('-'):
                arr.append(int(val))
            if tuple(arr) >= tuple(result):
                is_find_val = 1
                data_array.append(str(rec["number"]) + "          " + str(rec["state"]) + "   "
                                  + str(rec["user"]["login"]) + "        " + str(rec["created_at"]) + "        "
                                  + str(rec["title"]))
    if is_find_val == 0:
        print("No such data")
    else:
        print("req.number  state  user          created                           title")
        for i in data_array:
            print(i)


def obd(res, string_date):
    is_find_val = 0
    result = []
    data_array = []
    str_d = string_date.split("-")
    for val in str_d:
        result.append(int(val))
    for rec in res:
        if rec["state"] == "open":
            arr = []
            for val in rec["created_at"].split("T")[0].split('-'):
                arr.append(int(val))
            if tuple(arr) <= tuple(result):
                is_find_val = 1
                data_array.append(str(rec["number"]) + "          " + str(rec["state"]) + "   "
                                  + str(rec["user"]["login"]) + "        " + str(rec["created_at"]) + "        "
                                  + str(rec["title"]))
    if is_find_val == 0:
        print("No such data")
    else:
        print("req.number  state  user          created                           title")
        for i in data_array:
            print(i)


def ncc(res):
    print("Pull request info:")
    print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
          + ". Number of comments: " + str(res["comments"]))


def ndo(res):
    date_arr = []
    for val in res["created_at"].split("T")[0].split('-'):
        date_arr.append(int(val))

    now = datetime.datetime.now()
    d0 = date(date_arr[0], date_arr[1], date_arr[2])
    d1 = date(now.year, now.month, now.day)
    delta = d0 - d1
    print("Opened days info:")
    print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
          + ". Days opened: " + str(abs(delta.days)))


def dwo(res):
    week = ['Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday']
    date_arr = []
    for val in res["created_at"].split("T")[0].split('-'):
        date_arr.append(int(val))
    print("Day of week opened:")
    print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
          + ". Day opened: " + str(week[date(date_arr[0], date_arr[1], date_arr[2]).weekday()]))


def dwc(res):
    if res["closed_at"]:
        week = ['Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday']
        date_arr = []
        for val in res["closed_at"].split("T")[0].split('-'):
            date_arr.append(int(val))
        print("Day of week opened:")
        print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
              + ". Day closed: " + str(week[date(date_arr[0], date_arr[1], date_arr[2]).weekday()]))
    else:
        print("Day of week closed:")
        print("Request still not closed.")


def wo(res):
    date_arr = []
    for val in res["created_at"].split("T")[0].split('-'):
        date_arr.append(int(val))
    print("Week in year:")
    print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
          + ". Week opened: " + str(datetime.date(date_arr[0], date_arr[1], date_arr[2]).isocalendar()[1]))


def wc(res):
    if res["closed_at"]:
        date_arr = []
        for val in res["created_at"].split("T")[0].split('-'):
            date_arr.append(int(val))
        print("Week in year:")
        print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
              + ". Week opened: " + str(datetime.date(date_arr[0], date_arr[1], date_arr[2]).isocalendar()[1]))
    else:
        print("Week in year:")
        print("Request still not closed.")


def uo(res):
    print("User opened:")
    print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
          + ". Opened by user: " + str(res["user"]["login"]))


def uc(res):
    if res["state"] == "closed":
        response = requests.get('https://api.github.com/repos/' + args.username[0] + '/' + args.repository[0] +
                                '/issues/' + args.number + '/events', auth=authen)
        if (response.ok):
            js = json.loads(response.text)
            print("User closed request:")
            print("PR num: " + str(res["number"]) + "   " + str(res["state"]) + "   " + str(res["user"]["login"])
                  + ". User closed request: " + str(js[0]["actor"]["login"]))
    else:
        print("User closed request:")
        print("Request still not closed.")

def al(res):
    response = requests.get('https://api.github.com/repos/' + args.username[0] + '/' + args.repository[0] +
                            '/issues/' + args.number + '/events', auth=authen)
    if (response.ok):
        js = json.loads(response.text)
        for i in js:
            if "label" in i:
                print("Label for PR " + str(res["number"]) + ". Label = " +i["label"]["name"])


def nla(res):
    print("Number lines added:")
    print(res["additions"])


def nld(res):
    print("Number lines deleted:")
    print(res["deletions"])


def hdc(res):
    if res["closed_at"]:
        print("Hour of day closed:")
        hms = res["created_at"].split("T")[1].split('-')
        print(hms[0].split(":")[0])


def hdo(res):
    if res["created_at"]:
        print("Hour of day opened:")
        hms = res["created_at"].split("T")[1].split('-')
        print(hms[0].split(":")[0])


def ghub_request(type=""):
    response = requests.get('https://api.github.com/repos/' + args.username[0] + '/' + args.repository[0] +
                            '/pulls?state=' + type, auth=authen)
    if (response.ok):
        return json.loads(response.text)
    else:
        print("ERR: Something goes wrong. Please check username, repository name, options.")
        exit()


def ghub_num_request():
    response = requests.get('https://api.github.com/repos/' + args.username[0] + '/' + args.repository[0] +
                            '/pulls/' + args.number, auth=authen)
    if (response.ok):
        return json.loads(response.text)
    else:
        print("ERR: Something goes wrong. Please check username, repository name, pull request number options.")
        exit()


# ------------------------------------- getting data from GitHub api ------------------------------------------------- #

num_opts = ["ndo", "dwo", "dwc", "wo", "wc", "uo", "uc", "al", "nla", "nld", "hdc", "hdo", "ncc"]
gen_opts = ["bs"]


if args.number:
    if args.options:
        data = ghub_num_request()
        for i in args.options:
            if i in num_opts:
                globals()[i](data)
    else:
        summary_single_inf(ghub_num_request())
else:
    if args.opened_after_date:
        oad(ghub_request("open"), args.opened_after_date)
        exit()
    if args.opened_before_date:
        obd(ghub_request("open"), args.opened_before_date)
        exit()
    if args.options:
        for i in args.options:
            if i in gen_opts:
                globals()[i](ghub_request("all"))
            else:
                summary_rep_inf(ghub_request("all"))
    else:
        summary_rep_inf(ghub_request("all"))
