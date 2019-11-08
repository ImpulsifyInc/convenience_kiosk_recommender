# Demonstrates Bootstrap version 3.3 Starter Template
# available here: https://getbootstrap.com/docs/3.3/getting-started/#examples

from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import psycopg2 as pg2
import pandas.io.sql as sqlio
import sys
sys.path.append("..")
from src.get_clusters import get_table
from src.category_recommender import sold_by_store, top_sold_by_cluster, top_sold_overall, compare_products

app = Flask(__name__)

#sold = get_table('SELECT * FROM product_category_recommender')
sql = 'SELECT DISTINCT property_code FROM product_category_recommender ORDER BY property_code'
prop_list = list(get_table(sql).iloc[:,0])
sql = 'SELECT DISTINCT transaction_month FROM product_category_recommender ORDER BY transaction_month DESC'
month_list = list(get_table(sql).iloc[:,0])
sql = 'SELECT DISTINCT category_name FROM product_category_recommender ORDER BY category_name'
category_list = list(get_table(sql).iloc[:,0])
#number_category_list = ['a','b']#[5, 1, 2, 3, 4, 6, 7, 8, 9, 10]

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    properties = prop_list #['CLTTB', 'DALLF', 'LRDES', 'DTTLI', 'CHILM', 'SEALW','MEMPE', 'MIASP', 'YULDN', 'MCOOR']
    categories = category_list
    months = month_list
    nums = [5, 1, 2, 3, 4, 6, 7, 8, 9, 10]
    return render_template('index.html', properties = properties, categories = categories, months = months, nums = nums)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    property = request.form['property'] 
    category = request.form['category']
    month = request.form['month']
    num = request.form['num']
    
    SQL = """SELECT * 
            FROM product_category_recommender 
            WHERE property_code = '{0}'
                AND category_name = '{1}'
            """.format(property, category)
    sold = get_table(SQL)

    recommendation = compare_products(property, category, month, int(num), sold)

    return render_template('recommend.html', property=property, recommendation=recommendation)

@app.route('/property_lookup')
def property_lookup():
    prop_lookup = get_table('SELECT * FROM property_code_lookup')
    return render_template('property_lookup.html', data = prop_lookup.to_html())

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
