#!/usr/bin/env python
import os
import io
import json
# import xlsxwriter
from flask import Flask, render_template, request, Response, send_file, make_response
from get_data import main_get_data

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
		response=request.data
		print('response', response)
		str_response = response.decode('utf-8')
		print('decode', str_response)
		new_dict = json.loads(str_response)
		#print("symbols type from form", type(parameters['symbols']))
		#new_dict = parameters.to_dict()
		new_dict['symbols'] = new_dict['symbols'].split(",")
		print("new_dict", new_dict)
		# csv = some_data(new_dict)
		xlsx = main_get_data(new_dict)
		"""response = make_response(xlsx)
		response.headers["Content-disposition"] = "attachment; filename={0}.xlsx".format(new_dict['filename'])
		return response"""
		return Response(
	        xlsx,
	        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	        headers={"Content-disposition":
	                 "attachment; filename={0}.xlsx".format(new_dict['filename'])}
        )

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 33507))
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    # app.run(debug=False, port=port)
    app.run(host='0.0.0.0', debug=True, port=port)
