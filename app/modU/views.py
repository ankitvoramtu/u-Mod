from modU import app
from flask import render_template,request,Flask
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
import cPickle as pickle
import sklearn.ensemble.forest
import os

import StringIO
import base64
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns

import ComplexRadar


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(APP_ROOT,'test.pickle')) as f:
  current_model = pickle.load(f)


class SubmissionForm(Form):
  comment = TextAreaField('comment')
  subreddit = StringField('sub reddit')


# Graphing Functions
# def predict_outcome (subreddit , comment):




#Route Handling

@app.route('/', methods=['GET','POST'])
def index():
  form = SubmissionForm()
  if request.method == "POST":
    subreddit = request.form['subreddit']
    comment = request.form['comment']



    variables = ("Normal Scale", "Inverted Scale", "Inverted 2",
                "Normal Scale 2", "Normal 3", "Normal 4 %",
                 "Normal Scale 2", "Normal 3", "Normal 4 %")

    data = (0.5, 0.75, 0.8,
            0.5, 0.75, 0.8,
            0.5, 0.75, 0.8)

    ranges = [(1e-31, 1),(1e-31, 1), (1e-31, 1),
              (1e-31, 1),(1e-31, 1), (1e-31, 1),
              (1e-31, 1),(1e-31, 1), (1e-31, 1)]

    # plotting
    img = StringIO.StringIO()

    fig1 = plt.figure(figsize=(8, 8))
    radar = ComplexRadar.ComplexRadar(fig1, variables, ranges)
    radar.plot(data)
    radar.fill(data, alpha=0.2)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue())

    return render_template('report.html', plot_url=plot_url)




  return render_template('index.html',
                          title='/u/Mod',
                          form=form
                          )


