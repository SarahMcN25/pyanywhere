# This program creates an application server that will implement a RESTful API. 
# Author: Sarah McNelis - G00398343

# Code adapted from W8 lecture and labs: <https://web.microsoftstream.com/video/c575feed-7ee1-4eec-b70e-c1b49204146c?list=studio> 


from flask import Flask, url_for, request, redirect, abort, jsonify
from arrivalsDAO import arrivalsDAO


app = Flask(__name__, static_url_path='', static_folder='static')


# Arrivals array
arrivals=[
        {"id":1, "airline":"AerLingus", "origin": "JFK", "destination":"SNN", "flightnumber":"EI110" },
        {"id":2, "airline":"Ryanair", "origin": "STN", "destination":"SNN", "flightnumber":"FR310" },
        {"id":3, "airline":"AerLingus", "origin": "LHR", "destination":"SNN", "flightnumber":"EI381" },
        {"id":4, "airline":"Air Canada", "origin": "YYZ", "destination":"SNN", "flightnumber":"AC856" }, 
        {"id":5, "airline":"Ryanair", "origin": "LGW", "destination":"SNN", "flightnumber":"FR1183" },
        {"id":6, "airline":"Delta Airlines", "origin": "JFK", "destination":"SNN", "flightnumber":"DL206" },
        {"id":7, "airline":"American Airlines", "origin": "PHL", "destination":"SNN", "flightnumber":"AA089" },
        {"id":8, "airline":"Lufthansa", "origin": "FRA", "destination":"SNN", "flightnumber":"LH8045" }, 
        {"id":9, "airline":"United Airlines", "origin": "EWR", "destination":"SNN", "flightnumber":"UA022" },
        {"id":10, "airline":"Ryanair", "origin": "MAN", "destination":"SNN", "flightnumber":"FR8159" },
        {"id":11, "airline":"Ryanair", "origin": "FUE", "destination":"SNN", "flightnumber":"FR3369" }
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