# This program creates an flask application server that will implement a RESTful API. 
# Author: Sarah McNelis - G00398343

# Code adapted from W8 lecture and labs


from flask import Flask, url_for, request, redirect, abort, jsonify
from airportDAO import arrivalsDAO, departuresDAO


app = Flask(__name__, static_url_path='', static_folder='static')


# Arrivals array
arrivals=[
        {"id":1, "airline":"AerLingus", "origin": "JFK", "destination":"SNN", "flightnumber":"EI110", "scheduledarrival":"0605", "actualarrival":"0716"},
        {"id":2, "airline":"Ryanair", "origin": "STN", "destination":"SNN", "flightnumber":"FR310", "scheduledarrival":"0645", "actualarrival":"0722" },
        {"id":3, "airline":"AerLingus", "origin": "LHR", "destination":"SNN", "flightnumber":"EI381", "scheduledarrival":"0920", "actualarrival":"0943" },
        {"id":4, "airline":"Air Canada", "origin": "YYZ", "destination":"SNN", "flightnumber":"AC856", "scheduledarrival":"0950", "actualarrival":"1016" }, 
        {"id":5, "airline":"Ryanair", "origin": "LGW", "destination":"SNN", "flightnumber":"FR1183", "scheduledarrival":"1115", "actualarrival":"1124" },
        {"id":6, "airline":"Delta Airlines", "origin": "JFK", "destination":"SNN", "flightnumber":"DL206", "scheduledarrival":"1205", "actualarrival":"1201" },
        {"id":7, "airline":"American Airlines", "origin": "PHL", "destination":"SNN", "flightnumber":"AA089", "scheduledarrival":"1440", "actualarrival":"1435" },
        {"id":8, "airline":"Lufthansa", "origin": "FRA", "destination":"SNN", "flightnumber":"LH8045", "scheduledarrival":"1505", "actualarrival":"1456" }, 
        {"id":9, "airline":"United Airlines", "origin": "EWR", "destination":"SNN", "flightnumber":"UA022", "scheduledarrival":"1630", "actualarrival":"1657" },
        {"id":10, "airline":"Ryanair", "origin": "MAN", "destination":"SNN", "flightnumber":"FR8159", "scheduledarrival":"1815", "actualarrival":"1742" },
        {"id":11, "airline":"Ryanair", "origin": "FUE", "destination":"SNN", "flightnumber":"FR3369", "scheduledarrival":"2030", "actualarrival":"2150" }
        ]


# Departures array
departures=[
        {"id":1, "airline":"Ryanair", "origin": "SNN", "destination":"LPA", "flightnumber":"FR8170", "scheduleddeparture":"0610", "actualdeparture":"0653"},
        {"id":2, "airline":"Ryanair", "origin": "SNN", "destination":"STN", "flightnumber":"FR311", "scheduleddeparture":"0735", "actualdeparture":"0755" },
        {"id":3, "airline":"AerLingus", "origin": "SNN", "destination":"LHR", "flightnumber":"EI380", "scheduleddeparture":"0750", "actualdeparture":"0838" },
        {"id":4, "airline":"Air Canada", "origin": "SNN", "destination":"YYZ", "flightnumber":"AC825", "scheduleddeparture":"1030", "actualdeparture":"1105" }, 
        {"id":5, "airline":"AerLingus", "origin": "SNN", "destination":"JFK", "flightnumber":"EI214", "scheduleddeparture":"1145", "actualdeparture":"1153" },
        {"id":6, "airline":"Delta Airlines", "origin": "SNN", "destination":"ATL", "flightnumber":"DL408", "scheduleddeparture":"1210", "actualdeparture":"1216" },
        {"id":7, "airline":"American Airlines", "origin": "SNN", "destination":"PHL", "flightnumber":"AA065", "scheduleddeparture":"1345", "actualdeparture":"1420" },
        {"id":8, "airline":"Lufthansa", "origin": "SNN", "destination":"FRA", "flightnumber":"LH8105", "scheduleddeparture":"1425", "actualdeparture":"1415" }, 
        {"id":9, "airline":"United Airlines", "origin": "SNN", "destination":"EWR", "flightnumber":"UA015", "scheduleddeparture":"1700", "actualdeparture":"1743" },
        {"id":10, "airline":"Ryanair", "origin": "SNN", "destination":"MAN", "flightnumber":"FR8248", "scheduleddeparture":"1730", "actualdeparture":"1747" },
        {"id":11, "airline":"Ryanair", "origin": "SNN", "destination":"FUE", "flightnumber":"FR3279", "scheduleddeparture":"2230", "actualdeparture":"2318" }
        ]

 
nextId = 12 


# TEST
@app.route('/')
def index():
    return "hello"


# GET ALL ARRIVALS
# curl http://127.0.0.1:5000/arrivals
@app.route('/arrivals', methods=['GET'])
def getAllArrivals():
    #return "served by Get All()" #debug
    return jsonify(arrivals)


# GET ALL DEPARTURES
# curl http://127.0.0.1:5000/departures
@app.route('/departures', methods=['GET'])
def getAllDepartures():
    #return "served by Get All()" #debug
    return jsonify(departures)


# CREATE AN ARRIVAL
# curl -X POST -H "content-type:application/json" -d "{\"airline\":\"EasyJet\", \"origin\":\"CDG\", \"destination\":\"SNN\", \"flightnumber\":\"EZY6771\", \"scheduledarrival\":\"1615\", \"actualarrival\":\"1620\"}"  http://127.0.0.1:5000/arrivals
@app.route('/arrivals', methods=['POST'])
def createArrival():
    #return "served by create()" # debug

    global nextId

    if not request.json:
        abort(400)

    arrival = {
        "id":nextId, 
        "airline": request.json["airline"], 
        "origin": request.json["origin"],
        "destination": request.json["destination"],
        "flightnumber": request.json["flightnumber"],
        "scheduledarrival": request.json["scheduledarrival"],
        "actualarrival": request.json["actualarrival"]
    }
    newArrival = arrivalsDAO.createArrival(arrival)
    # Append to arrivals, up an id and return in json form. 
    #arrivals.append(arrival)
    nextId += 1
    return jsonify(newArrival)


# CREATE AN DEPARTURE
# curl -X POST -H "content-type:application/json" -d "{\"airline\":\"EasyJet\", \"origin\":\"SNN\", \"destination\":\"CDG\", \"flightnumber\":\"EZY6771\", \"scheduleddeparture\":\"2106\", \"actualdeparture\":\"2210\"}"  http://127.0.0.1:5000/departures
@app.route('/departures', methods=['POST'])
def createDeparture():
    #return "served by create()" # debug

    global nextId

    if not request.json:
        abort(400)

    departure = {
        "id":nextId, 
        "airline": request.json["airline"], 
        "origin": request.json["origin"],
        "destination": request.json["destination"],
        "flightnumber": request.json["flightnumber"],
        "scheduleddeparture": request.json["scheduleddeparture"],
        "actualdeparture": request.json["actualdeparture"]
    }
    newDeparture = departuresDAO.createDeparture(departure)
    # Append to departures, up an id and return in json form. 
    #departures.append(departure)
    nextId += 1
    return jsonify(newDeparture)


# UPDATE AN ARRIVAL
#  curl -X PUT -H "content-type:application/json" -d "{\"airline\":\"Lufthansa\", \"origin\":\"FRA\", \"destination\":\"SNN\", \"flightnumber\":\"LH401\", \"scheduledarrival\":\"1015\", \"actualarrival\":\"1130\"}"  http://127.0.0.1:5000/arrivals/1
@app.route('/arrivals/<int:id>', methods=['PUT'])
def updateArrival(id):
    #return "served by update with id " + str(id) #debug

    foundArrivals = list(filter (lambda t : t["id"]== id, arrivals))

    if len(foundArrivals) == 0:
        return jsonify({}), 404

    currentArrival = arrivalsDAO.findByID(foundArrivals[0])
    #currentArrival = foundArrivals[0]

    if 'Airline' in request.json:
        currentArrival['airline'] = request.json['airline']

    if 'Origin' in request.json:
        currentArrival['origin'] = request.json['origin']
            
    if 'Destination' in request.json:
        currentArrival['destination'] = request.json['destination']

    if 'Flight Number' in request.json:
        currentArrival['flightnumber'] = request.json['flightnumber']

    if 'Scheduled Arrival' in request.json:
        currentArrival['scheduledarrival'] = request.json['scheduledarrival']

    if 'Actual Arrival' in request.json:
        currentArrival['actualarrival'] = request.json['actualarrival']

    return jsonify(currentArrival)


# UPDATE AN DEPARTURE
#  curl -X PUT -H "content-type:application/json" -d "{\"airline\":\"Lufthansa\", \"origin\":\"SNN\", \"destination\":\"FRA\", \"flightnumber\":\"LH401\", \"scheduleddeparture\":\"1722\", \"actualdeparture\":\"1740\"}"  http://127.0.0.1:5000/departures/1
@app.route('/departures/<int:id>', methods=['PUT'])
def updateDeparture(id):
    #return "served by update with id " + str(id) #debug

    foundDepartures = list(filter (lambda t : t["id"]== id, departures))

    if len(foundDepartures) == 0:
        return jsonify({}), 404

    currentDeparture = departuresDAO.findByID(foundDepartures[0])
    #currentDeparture = foundDepartures[0]

    if 'Airline' in request.json:
        currentDeparture['airline'] = request.json['airline']

    if 'Origin' in request.json:
        currentDeparture['origin'] = request.json['origin']
            
    if 'Destination' in request.json:
        currentDeparture['destination'] = request.json['destination']

    if 'Flight Number' in request.json:
        currentDeparture['flightnumber'] = request.json['flightnumber']

    if 'Scheduled Departure' in request.json:
        currentDeparture['scheduleddeparture'] = request.json['scheduleddeparture']

    if 'Actual Departure' in request.json:
        currentDeparture['actualdeparture'] = request.json['actualdeparture']

    return jsonify(currentArrival)


# DELETE AN ARRIVAL
# curl -X DELETE http://127.0.0.1:5000/arrivals/1
@app.route('/arrivals/<int:id>', methods=['DELETE'])
def deleteArrival(id):
    #return "served by delete with id " + str(id) #debug

    foundArrivals = list(filter (lambda t : t["id"]== id, arrivals))

    if len(foundArrivals) == 0:
        return jsonify({}), 404

    arrivalsDAO.deleteArrival(foundArrivals[0])

    return jsonify({"done":True})


# DELETE AN DEPARTURE
# curl -X DELETE http://127.0.0.1:5000/departures/1
@app.route('/departures/<int:id>', methods=['DELETE'])
def deleteDeparture(id):
    #return "served by delete with id " + str(id) #debug

    foundDepartures = list(filter (lambda t : t["id"]== id, departures))

    if len(foundDepartures) == 0:
        return jsonify({}), 404

    departuresDAO.deleteDeparture(foundDepartures[0])

    return jsonify({"done":True})


# RUN THE PROGRAM
if __name__ == "__main__":
    app.run(debug=True)