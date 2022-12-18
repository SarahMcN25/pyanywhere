# This file contains two classes - one for arrivals, one for departures - 
# These classes contain functions to implement SQL commands to my database from this python script. 
# These classes will be imported and used in rest_server.py
# Author: Sarah McNelis - G00398343

# Code adapted from W9 lecture and labs


import mysql.connector
import config as cfg


# ARRIVALS CLASS
class ArrivalsDAO:
    host = ""
    user = ""
    password = ""
    database = ""
    connection = ""
    cursor = ""


    # GET CONFIG DETAILS
    def __init__(self): 
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
    

    # GET CURSOR - MAKE CONNECTION 
    def getCursor(self): 
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor


    # CLOSE CURSOR AND CONNECTION
    def closeAll(self):
        self.connection.close()
        self.cursor.close()


    # GET ALL ARRIVALS
    def getAllArrivals(self):
        cursor = self.getCursor()
        sql="SELECT * FROM arrivals"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeAll()
        return result


    # CREATE AN ARRIVAL
    def createArrival(self, values):
        cursor = self.getCursor()
        sql="INSERT INTO arrivals (airline, origin, destination, flight_number, scheduled_arrival, actual_arrival) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid


    # UPDATE ARRIVAL
    def updateArrival(self, values):
        cursor = self.getCursor()
        sql="UPDATE arrivals SET airline=%s, origin=%s, destination=%s, flight_number=%s, scheduled_arrival=%s, actual_arrival=%s WHERE id=%s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()


    # DELETE ARRIVAL
    def deleteArrival(self, id):
        cursor = self.getCursor()
        sql="DELETE FROM arrivals WHERE id=%s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll
        print("Arrival deleted") 

    
    # CREATE A DATABASE
    def createDatabase(self):
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql="CREATE DATABASE "+ self.database
        self.cursor.execute(sql)
        self.connection.commit()
        self.closeAll()


    # CREATE A DATABASE TABLE
    def createTable(self):
        cursor = self.getcursor()
        sql="CREATE TABLE arrivals (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, airline varchar(50), origin varchar(3), destination varchar(3), flight_number varchar(10), scheduled_arrival varchar(4), actual_arrival varchar(4))"
        cursor.execute(sql)
        self.connection.commit()
        self.closeAll()


# Var to be imported to rest_server.py
arrivalsDAO = ArrivalsDAO()


# DEPARTURES CLASS
class DeparturesDAO:
    host = ""
    user = ""
    password = ""
    database = ""
    connection = ""
    cursor = ""


    # GET CONFIG DETAILS
    def __init__(self): 
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
    

    # GET CURSOR - MAKE CONNECTION 
    def getCursor(self): 
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor


    # CLOSE CURSOR AND CONNECTION
    def closeAll(self):
        self.connection.close()
        self.cursor.close()


    # GET ALL DEPARTURES
    def getAllDepartures(self):
        cursor = self.getCursor()
        sql="SELECT * FROM departures"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeAll()
        return result


    # CREATE AN DEPARTURES
    def createDeparture(self, values):
        cursor = self.getCursor()
        sql="INSERT INTO departures (airline, origin, destination, flight_number, scheduled_departure, actual_departure) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid


    # UPDATE DEPARTURES
    def updateDeparture(self, values):
        cursor = self.getCursor()
        sql="UPDATE departures SET airline=%s, origin=%s, destination=%s, flight_number=%s, scheduled_departure=%s, actual_departure=%s WHERE id=%s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()


    # DELETE DEPARTURES
    def deleteDeparture(self, id):
        cursor = self.getCursor()
        sql="DELETE FROM departures WHERE id=%s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll
        print("Departure deleted") 


    # CREATE A DATABASE TABLE
    def createTable(self):
        cursor = self.getcursor()
        sql="CREATE TABLE departures (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, airline varchar(50), origin varchar(3), destination varchar(3), flight_number varchar(10), scheduled_departure varchar(4), actual_departure varchar(4))"
        cursor.execute(sql)
        self.connection.commit()
        self.closeAll()


# Var to be imported to rest_server.py
departuresDAO = DeparturesDAO()


'''
# MAIN FUNCTION
 if __name__ == "__main__":
    # Once off setting up DB and table
#   arrivalsDAO.createDatabase()
#   arrivalsDAO.createTable()
#   departuresDAO.createTable()
    # TESTING DATA
    data1 = ('British Airways', 'BHX', 'SNN', 'BA6774', "0900", "1030")
    data2 = ('British Airways', 'SNN', 'BHX', 'BA7255', "2100", "2105")
    arrivalsDAO.create(data1)
    print("It works!")
    departuresDAO.create(data2)
    print("It works!")
'''