from __future__ import absolute_import, division, print_function, unicode_literals
import os

# !pip install -q colabcode #REMEMBER
# !pip install jinja2==2.11.3
# !pip install flask
# #!pip install flask-ngrok

# from colabcode import ColabCode

#no Auth please
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import process
import pickle
import joblib
#from flask_ngrok import run_with_ngrok
from flask import Flask, request, render_template
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

#run_with_ngrok(app)
# load the data from disk
loaded_norm_data = pickle.load(open('normalized_data_file', 'rb'))

loaded_title_data = pickle.load(open('title_names_file', 'rb'))

normalized_data = loaded_norm_data
title_names = loaded_title_data

@app.route('/')
def home():
    return render_template('/startup2-1.0.0/iindex.html')
    # return redirect(url_for('/startup2-1.0.0/iindex.html'))

@app.route('/quote')
def quote():
    return render_template('/startup2-1.0.0/quote.html')

@app.route('/contact')
def contact():
    return render_template('/startup2-1.0.0/contact.html')

@app.route('/recommendation',methods=['POST'])
def recommendation():

  def recommendations(a):
    neighbor_index = knn.kneighbors([normalized_data.loc[a]], return_distance=False, n_neighbors=11)
    neighbor_index = list(neighbor_index[0])
    neighbor_index = neighbor_index[1:11]
    print("Recommendations for: " + title_names.loc[a, 'title'])
    print(title_names.loc[neighbor_index])

  netflix_titles = list(title_names.loc[:, 'title'])

  def movie(title):
    title = title.lower()
    result = process.extract(title, netflix_titles, limit = 5)
    i = 1
    for mov in result:
      if (i == 1 and mov[1] <= 80):
        print('No close matches found. Try again.')
        break
      if mov[1] == 100:
        index = netflix_titles.index(title)
        recommendations(index)
        return
      if (mov[1] >= 80 and mov[1] != 100):
        if i == 1:
          print('Exact match not found for {}. Did you mean:'.format(title))
        print(str(i) + ') ' + mov[0])
        i = i+1

  keys = request.form.keys()
  # keys = sorted(keys)

  for key in keys:
      print(key, request.form[key])
      for i in request.form[key]:
        print(movie(key))
      # print(key, request.form.get(key)

  return render_template('/startup2-1.0.0/quote.html', output=movie(key))
  # return redirect(output='Prediction is "{} Days" ({:.1f}%)'.format(DAYS[class_id], 100 * probability))
app.run()
