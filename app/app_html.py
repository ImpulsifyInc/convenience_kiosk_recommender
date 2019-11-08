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
from src.yo import yo

app = Flask(__name__)

sold = get_table('SELECT * FROM product_category_recommender')
sql = 'SELECT DISTINCT property_code FROM product_category_recommender ORDER BY property_code'
prop_list = list(get_table(sql).iloc[:,0])
sql = 'SELECT DISTINCT transaction_month FROM product_category_recommender ORDER BY transaction_month DESC'
month_list = list(get_table(sql).iloc[:,0])

number_category_list = [5, 1, 2, 3, 4, 6, 7, 8, 9, 10]

@app.route('/')
def index():
    display_str =   '''<h1>Welcome to the Product Recommender!<br></h1>
                        Please elect your options below:<br><br>
                    '''
    property = ['CLTTB', 'DALLF', 'LRDES', 'DTTLI', 'CHILM', 'SEALW','MEMPE', 'MIASP', 'YULDN', 'MCOOR']
    sql = 'SELECT DISTINCT category_name FROM product_category_recommender ORDER BY category_name'
    categories = list(get_table(sql).iloc[:,0])
    month = month_list
    num = number_category_list
    drop_downs =    '''
                    Property Code: <input type="text" name="property_code"> 
                    <br>
                    Category:
                    <select name="option" width="1000px">
                        {% for x in categories %}
                            <option value="{{ x }}"{% if loop.first %} SELECTED{% endif %}>{{ x }}</option>
                        {% endfor %}
                    </select>
                    <br>
                    Month:
                    <select>
                        {% for each in month %}
                        <option value="{{each}}">{{each}}</option>
                        {% endfor %}
                    </select>
                    <br>
                    '''


    go_to_recommend_html = '''
        <form action="/recommend" >
            <input type="submit" value = "Recommend Products!"/>
        </form>
    '''
    # html that gets returned
    return display_str + drop_downs + go_to_recommend_html 

# second routing block
@app.route('/submit') # if no methods specified, default is 'GET'
def submit():
    display_str = 'Paste in your text below:'
    # code below makes a button to go to the '/submit block
    return '''
        <form action="/predict" method='POST'>
          
          Submit your article for classification:<br>
          <input type="text" input style="height:200px; width: 500px" name="article"> 
          <br>
          <br><br>
          <input type="submit" value="Submit for class prediction">
        </form>
    '''
    
@app.route('/predict', methods = ["GET", "POST"])
def predict():
    display_str1 = 'This is the text you entered<br>'

    text = str(request.form['article'])

    display_str2 = '<br>It classifies as this topic:<br>'

    with open('data/model.pkl', 'rb') as f:
        model = pickle.load(f)

    X =request.form['article']

    topic = model.predict([X])
    top = topic[0]

    y = get_data('data/articles.csv')[1]

    display_str3 = '<br> Accuracy = '

    #print("Accuracy:", model.score(X, y))
    #print("Predictions:", model.predict(X))
    
    go_to_predict_html = '''
        <form action="/" >
            <input type="submit" value = "Return to home"/>
        </form>
    '''
    return display_str1 + str(text) + display_str2 + top + '<br>' + go_to_predict_html




@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # property = str(request.form['property'])
    # property_code = prop
    # product_category = prod_cat
    # month = mth
    # num_recommend = num
    #sold = get_table('SELECT * FROM product_category_recommender')
    #compare_products('SPICC', 'Beverage: Soda', '2019-09', 5)
    recommendation = compare_products('SPICC', 'Beverage: Soda', '2019-09', 5, df = sold)#compare_products(property, category, month)
    go_to_index_html = '''
        <br><br>
        <form action="/" >
            <input type="submit" value = "Return to home"/>
        </form>
    '''
    
    return 'recommendation = ' + recommendation + go_to_index_html

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
