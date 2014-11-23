#!/usr/bin/env python
from flask import Flask, render_template, Response
import rrdtool

app = Flask(__name__)

@app.route("/")
def hello():
	data = {}
	return render_template("index.html", **data);

@app.route("/graph.png")
def graph():
	ret = rrdtool.graph( "graph.png", "--start", "-1d", "--vertical-label=Bytes/s",
	"DEF:temp=../beer01.rrd:temp:AVERAGE",
	"DEF:light=../beer01.rrd:light:AVERAGE",
	"DEF:bubbles=../beer01.rrd:bubbles:AVERAGE",
	"LINE:temp#0000FF:Beer Temperature C",
	"LINE:light#00FF00:Beer light Lux",
	"LINE:bubbles#FF0000:Beer bubbles count",
	"COMMENT:\\n",
	"GPRINT:temp:AVERAGE:Avg temp\: %.2lfC",
	"COMMENT:  ",
	"GPRINT:temp:MAX:Max temp\: %.2lfC",
	"COMMENT: ",
	"GPRINT:temp:MIN:Min temp\: %.2lfC",
	"COMMENT:\\n",
	"GPRINT:light:AVERAGE:Avg light\: %.2lfLux",
	"COMMENT:  ",
	"GPRINT:light:MAX:Max light\: %.2lfLux",
	"COMMENT: ",
	"GPRINT:light:MIN:Min light\: %.2lfLux",
	"COMMENT:\\n",
	"GPRINT:bubbles:AVERAGE:Avg bubbles\: %.2lf",
	"COMMENT:  ",
	"GPRINT:bubbles:MAX:Max bubbles\: %.2lf",
	"COMMENT: ",
	"GPRINT:bubbles:MIN:Min bubbles\: %.2lf")
	data =""
	with open("graph.png","r") as file:
		data = file.read();
	

	return Response(data, mimetype="image/png");
	
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
