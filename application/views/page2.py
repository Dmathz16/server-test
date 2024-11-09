from flask import Blueprint, redirect, url_for, render_template, jsonify, session

import flask
import datetime
import random
import math

view_name = "page2"

page2 = Blueprint(view_name, __name__)

data = {}

@page2.route('/'+view_name+'/')
def index():
    
    data['subtitle'] = ''
    return render_template('page2/index.html', data=data)