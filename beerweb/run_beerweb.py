#!/usr/bin/env python
from flask import Flask, render_template, Response
import rrdtool

app = Flask(__name__)

@app.route("/")
def hello():
	data = {}
	return render_template("index.html", **data);

@app.route("/temp.png")
@app.route("/temp_<period>.png")
def temp(period="1d"):
	ret = rrdtool.graph( "temp.png", "--start", "-%s" % period, "--vertical-label=Temperature",
	"DEF:temp=../beer01.rrd:temp:AVERAGE",
	"LINE:temp#0000FF:Beer Temperature C",
	"COMMENT:\\n",
	"GPRINT:temp:AVERAGE:Avg temp\: %.2lfC",
	"COMMENT:  ",
	"GPRINT:temp:MAX:Max temp\: %.2lfC",
	"COMMENT: ",
	"GPRINT:temp:MIN:Min temp\: %.2lfC");
	data =""
	with open("temp.png","r") as file:
		data = file.read();
	

	return Response(data, mimetype="image/png");

@app.route("/light.png")
@app.route("/light_<period>.png")
def light(period="1d"):
	ret = rrdtool.graph( "light.png", "--start", "-%s" % period, "--vertical-label=Lux",
	"DEF:light=../beer01.rrd:light:AVERAGE",
	"LINE:light#00FF00:Beer light Lux",
	"COMMENT:\\n",
	"GPRINT:light:AVERAGE:Avg light\: %.2lfLux",
	"COMMENT:  ",
	"GPRINT:light:MAX:Max light\: %.2lfLux",
	"COMMENT: ",
	"GPRINT:light:MIN:Min light\: %.2lfLux")
	data =""
	with open("light.png","r") as file:
		data = file.read();
	

	return Response(data, mimetype="image/png");

@app.route("/bubbles.png")
@app.route("/bubbles_<period>.png")
def bubbles(period="1d"):
	ret = rrdtool.graph( "bubbles.png", "--start", "-%s" % period, "--vertical-label=Bubbles/minute",
	"DEF:bubbles=../beer01.rrd:bubbles:AVERAGE",
	"CDEF:bubblesmin=bubbles,6,/,60,*", # make it per minute
	"LINE:bubblesmin#FF0000:Beer bubbles count",
	"COMMENT:\\n",
	"GPRINT:bubblesmin:AVERAGE:Avg bubbles\: %.2lf/min",
	"COMMENT:  ",
	"GPRINT:bubblesmin:MAX:Max bubbles\: %.2lf/min",
	"COMMENT: ",
	"GPRINT:bubblesmin:MIN:Min bubbles\: %.2lf/min")
	data =""
	with open("bubbles.png","r") as file:
		data = file.read();
	

	return Response(data, mimetype="image/png");
	
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
