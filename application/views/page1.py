from flask import Blueprint, redirect, url_for, render_template, jsonify, session

import flask
import datetime
import random
import math

view_name = "page1"

page1 = Blueprint(view_name, __name__)

data = {}

@page1.route('/')
def welcome():
    data['subtitle'] = ''
    return render_template('page1/index.html', data=data)

@page1.route('/'+view_name+'/')
def index():
    
    data['subtitle'] = ''
    return render_template('page1/index.html', data=data)