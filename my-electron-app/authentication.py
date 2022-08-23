from flaskext.mysql import MySQL
from django.shortcuts import render
import os
import smtplib
import re
import sys
import sqlite3 as lite
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.graphics import BorderImage
from kivy.uix.dropdown import DropDown
from kivy.properties import BooleanProperty
import kivy.core.text.markup
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle #dfg
from datetime import datetime
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.app import App
import kivy
from urllib.request import urlopen
import requests
from flask import Flask, render_template, redirect, request, session
from json import dumps
from flask import jsonify, request, make_response, url_for, redirect
from json import dumps
from requests import post
from werkzeug.security import generate_password_hash
kivy.require('1.0.6')  # replace with your current kivy version !
import secrets
from flask_wtf.csrf import CSRFProtect




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.secret_key =secrets.token_bytes(16)
db = MySQL(app)

class MyApp(FloatLayout):
    """ Creates a Float Layout with  widgets and methods necessary
        for the Time Tracker application . """

    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        print(request.method)
        if request.method == "GET":
            print(request.method)
            return render_template("login.html")
        elif request.method == "POST":
            print(request.method)
            print("hhh")
            username = request.form["username"]
            print("email", username)
            password = request.form["password"]
            urls = 'http://localhost:8080/api/login/'
            myobj = {'username': username, 'password': password}
            x = requests.post(urls, data=myobj)
            session["username"] = request.form.get("username")
            print(x.status_code)
            if x.status_code == 200:
                session["credentials"] = request.form.get("username")
                return redirect("/get-data")
            else:
                return render_template("login.html")
    @app.route("/get-data", methods=['GET', 'POST'])
    def timers():
        print(request.method)
            
        if request.method == "POST":
            print("Check Date time", request.form["DateTime"])
            print('session', session.get('email'))
            if not 'StartDateTime' in request.form:
                start = request.form["DateTime"]
                # print(start, 'st')
                user_id = session["username"]
                print(user_id, 'usr')
                
                print(start)
                # print(stop, 'stp')
                urls = 'http://localhost:8080/accounts/time-api'
                myobj = {'start': start, 'user_id': user_id}
                # x = requests.post(urls, data=myobj)
                # print(x, 'akkkkk')
                return redirect(request.referrer)

                
            else:
                print("SESSION",request.session.get("user_id"))
                start = request.form["DateTime"]
                stop = request.form["StartDateTime"]
                timespent = request.form["timespent"]
                print(timespent, 'timespent save in db')
                user_id = session["username"]
                urls = 'http://localhost:8080/accounts/time-api'
                myobj = {'start': start, 'user_id': user_id, 'stop': stop, 'timespent':timespent}
                # x = requests.get(urls, data=myobj)
                # print(x)

                return redirect("/get-data")
        else:
          
            content = {'username':session["credentials"]}
            

            return render_template("index.html",**content)

    if __name__ == "__main__":
     
  
        app.secret_key =secrets.token_bytes(16)
        app.run(host='127.0.0.1', port=5000)
