from flask import Flask, request, url_for
from flask_cors import CORS, cross_origin
from flask_json import FlaskJSON, JsonError, json_response, as_json
import json
from flask import Response
from app import app
from models import MAIN
from app import db
from app import mysql

FlaskJSON(app)
CORS(app)


@app.route('/api/fetchData/', methods=['OPTIONS']) 
@cross_origin(origin='*')
def fetchDataOptions():
    print("fetchDataOptions")
    resp = Response(status=200)
    resp.headers['Access-Control-Max-Age'] = 86400
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/home/', methods=['GET', 'POST'])
@cross_origin(origin='*') 
def home():
    print(home)

    response = []
    response.append("dummy1")
    response.append("dummy2")
    ret = {
        'message': 'Flask API is deployed',
        'payload': response
    }
    js = json.dumps(ret)
    resp = Response(js, status=200, mimetype='application/json')
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    print("RESPONSE")
    print(resp)
    return resp


@app.route('/api/fetchData/', methods=['GET', 'POST'])
@cross_origin(origin='*')
def fetchData():
    print("fetchData")

    #Creating a connection cursor
    cursor = mysql.connection.cursor()

    query = "SELECT * FROM scholardb.MAIN"
    cursor.execute(query)

    response = []

    '''
        reference_link -> url
        reference_name -> title
    '''
    for(doi, url, year, publishers, authors, title, journal, fabrications, body_zones, materials, functions) in cursor:
        data_obj = {}
        data_obj["PIC ID"] = doi
        data_obj["Reference Link"] = url
        data_obj["Reference Name"] = title
        data_obj["Patents"] = ""
        data_obj["Research"] = ""
        data_obj["Source 1"] = ""
        data_obj["Tutorial"] = ""
        data_obj["Website"] = journal
        data_obj["Year"] = year
        data_obj["Display Name on the Picture if the name is too long?"] = ""
        data_obj["Design Concepts"] = "x"
        data_obj["Conference (VENUE)"] = publishers
        data_obj["Aesthetic Approach"] = ""
        data_obj["AUTHORS"] = authors

        fabricationArr = fabrications.split("++")
        if(len(fabricationArr) >= 2):
            data_obj["Fabrication 1"] = fabricationArr[0]
            data_obj["Fabrication 2"] = fabricationArr[1]
        elif(len(fabricationArr) == 1):
            data_obj["Fabrication 1"] = fabricationArr[0]
            data_obj["Fabrication 2"] = ""
        else:
            data_obj["Fabrication 1"] = ""
            data_obj["Fabrication 2"] = ""

        bodyZonesArr = body_zones.split("++")
        if(len(bodyZonesArr) >= 3):
            data_obj["Body Zone 1"] = bodyZonesArr[0]
            data_obj["Body Zone 2"] = bodyZonesArr[1]
            data_obj["Body Zone 3"] = bodyZonesArr[2]
        elif(len(bodyZonesArr) >= 2):
            data_obj["Body Zone 1"] = bodyZonesArr[0]
            data_obj["Body Zone 2"] = bodyZonesArr[1]
            data_obj["Body Zone 3"] = ""
        elif(len(bodyZonesArr) == 1):
            data_obj["Body Zone 1"] = bodyZonesArr[0]
            data_obj["Body Zone 2"] = ""
            data_obj["Body Zone 3"] = ""
        else:
            data_obj["Body Zone 1"] = ""
            data_obj["Body Zone 2"] = ""
            data_obj["Body Zone 3"] = ""

        materialsArr = materials.split("++")
        if(len(materialsArr) >= 3):
            data_obj["Material 1"] = materialsArr[0]
            data_obj["Material 2"] = materialsArr[1]
            data_obj["Material 3"] = materialsArr[2]
        elif(len(materialsArr) >= 2):
            data_obj["Material 1"] = materialsArr[0]
            data_obj["Material 2"] = materialsArr[1]
            data_obj["Material 3"] = ""
        elif(len(materialsArr) == 1):
            data_obj["Material 1"] = materialsArr[0]
            data_obj["Material 2"] = ""
            data_obj["Material 3"] = ""
        else:
            data_obj["Material 1"] = ""
            data_obj["Material 2"] = ""
            data_obj["Material 3"] = ""

        functionsArr = functions.split("++")
        if(len(functionsArr) >= 3):
            data_obj["Function 1"] = functionsArr[0]
            data_obj["Function 2"] = functionsArr[1]
            data_obj["Function 3"] = functionsArr[2]
        elif(len(functionsArr) >= 2):
            data_obj["Function 1"] = functionsArr[0]
            data_obj["Function 2"] = functionsArr[1]
            data_obj["Function 3"] = ""
        elif(len(functionsArr) == 1):
            data_obj["Function 1"] = functionsArr[0]
            data_obj["Function 2"] = ""
            data_obj["Function 3"] = ""
        else:
            data_obj["Function 1"] = ""
            data_obj["Function 2"] = ""
            data_obj["Function 3"] = ""

        response.append(data_obj)

    #Saving the Actions performed on the DB
    mysql.connection.commit()

    #Closing the cursor
    cursor.close()

    #fetch from SQL -> Convert to array

    ret = {
        'message': 'API connection established',
        'payload':response

    }

    js = json.dumps(ret)
    resp = Response(js, status=200, mimetype='application/json')
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    print("RESPONSE")
    print(resp)
    return resp
