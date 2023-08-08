#!/usr/bin/python
import re
import json
import web
from flask import Flask, request, jsonify
from flask.ext.script import Manager
from flask.ext.script import Server
#urls = ('/', 'index')
#app = web.application(urls, globals())

app = Flask(__name__)
@app.route('/<int:status_code>', methods=['GET'])
def get_median(status_code):
    p = re.compile(r'(([0-9]{1,3}\.){3}[0-9]{1,3})\s.\s.\s(\[([^\]])*])\s(\"[^\"]*")+((\s+\d+){2})')
    filename="logs.txt"
    f = open(filename)
    respsize = 0
    counter = 0
    print "Here's your file %r:" % filename
    #lines = f.readlines()
    with f as fs:
        for line in fs:
            #print line
            m = p.match(line)
            if m:
            #print "Match found", m.group(0)
            #print "Match found", m.group(1)
            #print "Match found", m.group(2)
            #print "Match found", m.group(3)
            #print "Match found", m.group(4)
            #print "Match found", m.group(5)
            #print "Match found", m.group(6)
                c = m.group(6).split(" ")
                #print c
                #print "status code %s size %s" % (c[1], c[2])
                if int(c[1]) == int(status_code):
                    print json.dumps({'median_size': int(c[2])},indent=4)
                    counter += 1
                    resp = int(c[2])
                    respsize = respsize + resp
                    print (respsize, counter)
                else:
                    print "No match"
    return json.dumps({'median_size': int(respsize)/int(counter)},indent=4)
man = Manager(app) 
man.add_command("runserver", Server(host="localhost", port=8888))
if __name__ == "__main__":
    man.run()
