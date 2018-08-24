from flask import Flask, redirect, url_for, request, abort
import atexit
import json
import time
import sms
import translate
from reverseGeocoding import get_taluka
import service_cloudant as dbclient
app = Flask(__name__)
from flask_cors import CORS, cross_origin
cors = CORS(app)



@atexit.register
def shutdown():
   dbclient.disconnect()
   
@app.route('/hello/<name>')
@cross_origin()
def hello(name):
    return 'welcome %s' % name

#@app.route('/',methods = ['POST', 'GET'])
#def login():
#    if request.method == 'POST':
#        number = request.form['number']
#        location = request.form['location']
#        severity = request.form['severity']
#        category = request.form['category']
#        quantity = request.form['quantity']
#        info = request.form['info']
#
#        return redirect(url_for('hello',name = user))
#    else:
#        user = request.args.get('name')
#        return redirect(url_for('hello',name = 'name')

@app.route('/test',methods = ['POST', 'GET'])
@cross_origin()
def test():
    if request.method == 'POST':
        print(request.headers)
        print(request.data)
        if not request.json:
            abort(400)
        print(request.json)
        return json.dumps(request.json)
    else:
        user = request.args.get('name')
        return 'hello %s' % user
   
@app.route('/requests',methods = ['POST', 'GET'])
@cross_origin()
def requests():
    if request.method == 'POST':
        print(request.data)
        if not request.json:
            abort(400)
        print(request.json)
        data = request.json
        if "location" in data:
            location = data["location"]
            lonlat = location.split(',')
            del data["location"]
            print(lonlat)
            locDetail = get_taluka(lonlat[0],lonlat[1])
            data['location'] = locDetail
            data['location']["requestLocation"] = lonlat
        else:
            print('ERROR : LOCATION not provided')
        localtime = int(time.time()) * 1000
        data["status"] = "NEW"
		data["translated_info"] = translate.convert(data["info"],'de-en')
        data["timestamp"] = {}
        data["timestamp"]["created"] = localtime
        data["timestamp"]["updated"] = localtime
        
        #write to db
        
        db = dbclient.createdb('request')
        dbclient.createdoc(db, data)
        
        return json.dumps(data)

@app.route('/requests/<id>',methods = ['PUT', 'GET'])
@cross_origin()
def putrequests(id):
    if request.method == 'PUT':
        print(request.data)
        if not request.json:
            abort(400)
        print(request.json)
        data = request.json
        db = dbclient.createdb('request')
        doc = dbclient.getres(db, id)
        print(doc)
        doc['status'] = "IN PROGRESS"
        dbclient.updateres(doc)
		
		
        sms.send_sms(doc['number'],"Your request has been update with: " + data['comment'])
        #translate
		
        return "SUCCESS"
        
@app.route('/location/<key>/requests',methods = ['POST', 'GET'])
@cross_origin()
def queryrequests(key):
    if request.method == 'GET':
        if key:
            key = key.lower()
        db = dbclient.createdb('request')
        result = dbclient.getresults(db,'get_location',key)
        print(result)
        return json.dumps(result['rows'])

@app.route('/location/<key>/counts',methods = ['POST', 'GET'])
@cross_origin()
def counts(key):
    if request.method == 'GET':
        if key:
            key = key.lower()
        db = dbclient.createdb('request')
        result = dbclient.getresults(db,'get_location',key)
        resultFF = dbclient.getresults(db,'get_requests_fulfilled',key)
        resultVol = dbclient.getresults(db,'get_volunteers',key,2)
        
        
        print(resultFF)
        print(resultVol)
        data = {}
        data['affected'] = 1000
        data['volunteers'] = 20
        data['requests'] = {}
        data['requests']['total'] = len(result['rows'])
        data['requests']['fulfilled'] = len(resultFF['rows'])
        
        return json.dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True, threaded=True)
