# This program creates an application server that will implement a RESTful API. 
# Author: Sarah McNelis - G00398343

# Code adapted from W8 lecture and labs: <https://web.microsoftstream.com/video/c575feed-7ee1-4eec-b70e-c1b49204146c?list=studio> 


from flask import Flask, url_for, request, redirect, abort, jsonify
from arrivalsDAO import arrivalsDAO


app = Flask(__name__, static_url_path='', static_folder='static')


# Arrivals array
arrivals=[
        {"ID":1, "Airline":"AerLingus", "Origin": "JFK", "Destination":"SNN", "Flight Number":"EI110" },
        {"ID":2, "Airline":"Ryanair", "Origin": "STN", "Destination":"SNN", "Flight Number":"FR310" },
        {"ID":3, "Airline":"AerLingus", "Origin": "LHR", "Destination":"SNN", "Flight Number":"EI381" },
        {"ID":4, "Airline":"Air Canada", "Origin": "YYZ", "Destination":"SNN", "Flight Number":"AC856" }, 
        {"ID":5, "Airline":"Ryanair", "Origin": "LGW", "Destination":"SNN", "Flight Number":"FR1183" },
        {"ID":6, "Airline":"Delta Airlines", "Origin": "JFK", "Destination":"SNN", "Flight Number":"DL206" },
        {"ID":7, "Airline":"American Airlines", "Origin": "PHL", "Destination":"SNN", "Flight Number":"AA089" },
        {"ID":8, "Airline":"Lufthansa", "Origin": "FRA", "Destination":"SNN", "Flight Number":"LH8045" }, 
        {"ID":9, "Airline":"United Airlines", "Origin": "EWR", "Destination":"SNN", "Flight Number":"UA022" },
        {"ID":10, "Airline":"Ryanair", "Origin": "MAN", "Destination":"SNN", "Flight Number":"FR8159" },
        {"ID":11, "Airline":"Ryanair", "Origin": "FUE", "Destination":"SNN", "Flight Number":"FR3369" }
        ]

 
nextId = 12 


# TEST
@app.route('/')
def index():
    return "hello"


# GET ALL ARRIVALS
# curl http://127.0.0.1:5000/arrivals
@app.route('/arrivals', methods=['GET'])
def getAll():
    #return "served by Get All()" #debug
    return jsonify(arrivals)


'''
# FIND ARRIVAL BY ID 
# curl http://127.0.0.1:5000/arrivals/2
@app.route('/arrivals/<int:id>', methods=['GET'])
def findById(id):
    #return "served by find by id with id " + str(id) # debug

    # Lambda searches arrivals and only return back specific id.
    foundArrivals = list(filter (lambda t : t["ID"]== id, arrivals))

    if len(foundArrivals) == 0:
        return jsonify({}), 204

    return jsonify(foundArrivals[0])
'''


# CREATE AN ARRIVAL
# curl -X POST -H "content-type:application/json" -d "{\"Airline\":\"EasyJet\", \"Origin\":\"CDG\", \"Destination\":\"SNN\", \"Flight Number\":\"EZY6771\"}"  http://127.0.0.1:5000/arrivals
@app.route('/arrivals', methods=['POST'])
def create():
    #return "served by create()" # debug

    global nextId

    if not request.json:
        abort(400)

    arrival = {
        "ID":nextId, 
        "Airline": request.json["Airline"], 
        "Origin": request.json["Origin"],
        "Destination": request.json["Destination"],
        "Flight Number": request.json["Flight Number"]
    }
    newArrival = arrivalsDAO.create(arrival)
    # Append to arrivals, up an id and return in json form. 
    #arrivals.append(arrival)
    nextId += 1
    return jsonify(newArrival)


# UPDATE AN ARRIVAL
#  curl -X PUT -H "content-type:application/json" -d "{\"Airline\":\"Lufthansa\", \"Origin\":\"FRA\", \"Destination\":\"SNN\", \"Flight Number\":\"LH401\"}"  http://127.0.0.1:5000/arrivals/1
@app.route('/arrivals/<int:id>', methods=['PUT'])
def update(id):
    #return "served by update with id " + str(id) #debug

    foundArrivals = list(filter (lambda t : t["ID"]== id, arrivals))

    if len(foundArrivals) == 0:
        return jsonify({}), 404

    currentArrival = arrivalsDAO.findByID(foundArrivals[0])
    #currentArrival = foundArrivals[0]

    if 'Airline' in request.json:
        currentArrival['Airline'] = request.json['Airline']

    if 'Origin' in request.json:
        currentArrival['Origin'] = request.json['Origin']
            
    if 'Destination' in request.json:
        currentArrival['Destination'] = request.json['Destination']

    if 'Flight Number' in request.json:
        currentArrival['Flight Number'] = request.json['Flight Number']

    return jsonify(currentArrival)


# DELETE AN ARRIVAL
# curl -X DELETE http://127.0.0.1:5000/arrivals/1
@app.route('/arrivals/<int:id>', methods=['DELETE'])
def delete(id):
    #return "served by delete with id " + str(id) #debug

    foundArrivals = list(filter (lambda t : t["ID"]== id, arrivals))

    if len(foundArrivals) == 0:
        return jsonify({}), 404

    arrivalsDAO.delete(foundArrivals[0])

    return jsonify({"done":True})


# RUN THE PROGRAM
if __name__ == "__main__":
    app.run(debug=True)