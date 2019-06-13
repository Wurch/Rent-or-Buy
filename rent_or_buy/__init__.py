from flask import Flask

import os
import json

with open('/etc/rent_buy_config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.secret_key = config.get('SECRET_KEY')

import rent_or_buy.routes
