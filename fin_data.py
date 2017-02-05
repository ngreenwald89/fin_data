#!/usr/bin/env python
import os
import json
from flask import Flask, render_template, request, Response, send_file, make_response
from get_data import main_get_data

app = Flask(__name__)

@app.route("/")
def parameters():
   return render_template('parameters.html')

@app.route('/result', methods = ['GET','POST'])
def result():
	if request.method == 'POST':
		response=request.data
		str_response = response.decode('utf-8')
		new_dict = json.loads(str_response)
		new_dict['symbols'] = new_dict['symbols'].split(",")
		xlsx = main_get_data(new_dict)
		return Response(
	        xlsx,
	        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	        headers={"Content-disposition":
	                 "attachment; filename={0}.xlsx".format(new_dict['filename'])}
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
