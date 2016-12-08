#!/usr/bin/env python
import os
from flask import Flask, render_template, request, Response, send_file
from get_data import some_data

app = Flask(__name__)

"""
@app.route("/")
def hello():
    return "Hello world!"
"""

@app.route("/")
def parameters():
   return render_template('parameters.html')

@app.route('/result', methods = ['GET','POST'])
def result():
	if request.method == 'POST':
		parameters = request.form
		print("symbols type from form", type(parameters['symbols']))
		new_dict = parameters.to_dict()
		new_dict['symbols'] = new_dict['symbols'].split(",")
		print("new_dict", new_dict)
		csv = some_data(new_dict)
		
		return Response(
	        csv,
	        mimetype="text/csv",
	        headers={"Content-disposition":
	                 "attachment; filename={0}.csv".format(new_dict['filename'])})

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 33507))
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    # app.run(debug=False, port=port)
    app.run(host='0.0.0.0', debug=True, port=port)
