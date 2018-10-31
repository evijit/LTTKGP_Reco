import sys
import os


from flask import Flask
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_session import Session
import json
import os
import numpy as np
from math import sqrt
from pymongo import MongoClient
from bson.json_util import dumps
from bson.json_util import loads as bloads

from getReco import get_reco, find_community


app = Flask(__name__)
sess = Session()

mc = MongoClient(os.environ['MONGODB_URI'])


def get_user_list():
    d = json.load(open("username2id.json", "r"))
    l = []
    for n in d.keys():
        if d[n] == "-1" or int(d[n]) == -1:
            continue
        if n == "nan":
            continue
        if "\\" in n:
            continue
        if int(find_community(int(d[n]))) == -1:
            continue
        l.append(n)
    l = sorted(l, key=str.lower)
    idlist = []
    for x in l:
        idlist.append(d[str(x)])
    return l, idlist


@app.route("/")
def main():
    user_list_toPass, idlist_toPass = get_user_list()
    # print(user_list_toPass)
    return render_template('index.html',
                           toPass=zip(user_list_toPass, idlist_toPass),
                           display_mode="display:none")


@app.route("/save", methods=['POST'])
def save():
    print("save")
    priority_list = request.values.getlist('result')
    username = request.values.getlist('username')[0]
    preference_list_coll = mc.get_default_database().preference_list

    try:
        if priority_list:
            print("adding...")
            preference_list_coll.insert_one({username: priority_list})
            print("added")
        else:
            print("priority_list is empty")
    except Exception as e:
        print("Error :- ")
        print(e)

    print(priority_list)
    return 'OK'

    # return "Thank You"

@app.route('/get_json')
def get_json():
    preference_list_coll = mc.get_default_database().preference_list
    cursor = preference_list_coll.find({})
    jsonList = []
    for document in cursor:
        jsonList.append(dumps(document))
    
    return jsonify({ 'json' : jsonList })

@app.route('/', methods=['POST'])
def get_pref_clicked():
    print("here")
    user_list_toPass, idlist_toPass = get_user_list()
    if request.form["submit_button"] == "Get Preference":
        uid = int(request.form["userid_selected"])
        print(uid)
        recos = get_reco(uid)
        reco_list_toPass = []
        for r in recos:
            reco_list_toPass.append(r[0])
        return render_template('index.html',
                               toPass=zip(user_list_toPass, idlist_toPass),
                               reco_list=reco_list_toPass,
                               display_mode="display:inline",
                               Uid=uid)

    if request.form["submit_button"] == "Submit":
        return render_template('index.html',
                               toPass=zip(user_list_toPass, idlist_toPass),
                               display_mode="display:none")
    return 'OK'


if __name__ == "__main__":
    app.secret_key = 'survey'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()
