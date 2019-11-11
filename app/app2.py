# Demonstrates Bootstrap version 3.3 Starter Template
# available here: https://getbootstrap.com/docs/3.3/getting-started/#examples

from flask import Flask, request, render_template
from flask_basicauth import BasicAuth
import pandas as pd
import numpy as np
import psycopg2 as pg2
import pandas.io.sql as sqlio
import sys
sys.path.append("..")
from src.get_clusters import get_table
from src.category_recommender import sold_by_store, top_sold_by_cluster, top_sold_overall, compare_products

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'un'
app.config['BASIC_AUTH_PASSWORD'] = 'pw'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

#sold = get_table('SELECT * FROM product_category_recommender')
sql = 'SELECT DISTINCT property_code FROM product_category_recommender ORDER BY property_code'
prop_list = list(get_table(sql).iloc[:,0])
sql = 'SELECT DISTINCT transaction_month FROM product_category_recommender ORDER BY transaction_month DESC'
month_list = list(get_table(sql).iloc[:,0])
sql = 'SELECT DISTINCT category_name FROM product_category_recommender ORDER BY category_name'
category_list = list(get_table(sql).iloc[:,0])

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    
    categories = category_list
    months = month_list
    nums = [5, 1, 2, 3, 4, 6, 7, 8, 9, 10]
    return render_template('index.html', categories = categories, months = months, nums = nums)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    property = request.form['property'] 
    category = request.form['category']
    month = request.form['month']
    num = request.form['num']
    
    SQL = """SELECT * 
            FROM product_category_recommender 
            WHERE transaction_month = '{0}'
            """.format(month)
    sold = get_table(SQL)

    recommendation = compare_products(property, category, month, int(num), sold)

    return render_template('recommend.html', property=property, recommendation=recommendation)

@app.route('/property_lookup', methods=['GET', 'POST'])

def property_lookup():
    sql = 'SELECT DISTINCT flag_name FROM product_category_recommender ORDER BY flag_name'
    flags = []
    flags.append(None)
    flags = flags + list(get_table(sql).iloc[:,0])
    sql = 'SELECT DISTINCT city FROM product_category_recommender ORDER BY city'
    cities = [None] + list(get_table(sql).iloc[:,0])
    sql = 'SELECT DISTINCT state FROM product_category_recommender ORDER BY state'
    states = [None] + list(get_table(sql).iloc[:,0])

    city = None
    state = None

    if request.method == 'POST':
        city = request.form['city']
        prop_lookup = get_table("SELECT * FROM property_code_lookup WHERE city = '{}' ".format(city))
    #     if request.form['city']:
    #         city = request.form['city']
    #     state = request.form['state']
    #     flag_name = request.form['flag_name']
    # if city != None:
    #     prop_lookup = get_table("SELECT * FROM property_code_lookup WHERE city = '{}' ".format(city))
    # if state != None:
    #     prop_lookup = get_table("SELECT * FROM property_code_lookup WHERE state = '{}' ".format(state))
    # if flag_name != None:
    #     prop_lookup = get_table("SELECT * FROM property_code_lookup WHERE flag_name = '{}' ".format(flag_name))
    else:
        prop_lookup = get_table('SELECT * FROM property_code_lookup')
    return render_template('property_lookup.html', data = prop_lookup.to_html(), \
        flags = flags, cities = cities, states = states)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
