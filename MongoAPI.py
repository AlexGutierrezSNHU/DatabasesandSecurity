#!/usr/bin/python
import json #imports json librabry
from bson import json_util#imports json_util from bson library
import bottle #import bottle from librabry
from bottle import route, run, request, abort, post, get, put, delete

from pymongo import MongoClient #Imports Mongo Client from Pymongo library

client = MongoClient('localhost', 27017) # sets local service and port	
db = client.market	#initializes db variable to mongodb Database
collection = db.stocks # initializes collection to mongodb Database Collection

#Method to create record
def createStock(value):

        try:
                document = {'Ticker' : value} # adds value in Json format
                result = collection.insert_one(document) # sets key value pair to called document

        except ValidationError as ve:
                abort(400, str(ve))# return HTTP error message

        return result # return new record

#Method to read record
def readStock(value):
        result = collection.find_one({ 'Ticker' : value})# calls document from collection

        if not result:
                abort(400, 'No document with TICKER %s found' % value)# return HTTP error message

        return result #return added document

#Method to update Record
def updateStock(key, value, document):
        post_input = collection.update({'Ticker': document}, {'$set':{key: value}}, upsert=False, multi=False) #sets key value pair to called document

        if not result:
                abort(400, 'No document with %s : %s' % key, value)# return HTTP error message

        return json.loads(json.dumps(result, indent=4, default=json_util.default)) #returns updated document in json format

#Method to delete Record		
def deleteStock(value):
        document = {'Ticker' : value} # adds value in Json format
        result = collection.delete_one(document) #deletes document based on key value pair

        if not result:
                abort(400, 'No document with TICKER : %s' % value)# return HTTP error message

        return result # return deleted record

#Method to call stock report
def sReport(list):
        result = []
        for value in list: #iterates through list
                record = collection.find_one({'Ticker': value}) #calls document with value
                for r in record: # Iterrates through documents
                        return r #returns document in json format

#method to call indutry report
def iReport(key):
        result = collection.aggregate([{'$match':{ "$Industry" : key}},#matches sectors
                {'$group': {'_id':{"Ticker" : "$Ticker", "Payout Ratio" : "$Payout Ratio", "Price": "$Price"}}}, #groups by ticker symbol, display payout ratio
                {'$sort': {"$Payout Ratio": -1}}, #sort in decending order
                {'$limit': 5}]) #limit to 5 documets

        return result #return documents


#createStock route
@route('/createStock/<value>',method='POST' )
def post_Stock(value):

        if not value:
                abort(400, 'No TICKER specified') # return HTTP error message

        try:
                createStock(value)#calls method and passes variable

        except ValidationError as ve:# return HTTP error message
                abort(400, str(ve))



#getStock route
@route('/getStock/<value>', method='GET')
def get_Stock(value):

        if not value:
                abort(400, 'No data received')# return HTTP error message

        try:
                readStock(value)#calls method and passes variable

        except ValidationError as ve:# return HTTP error message
                abort(400, str(ve))
	        
	if not ticker:
		abort(400, 'No data received')# return HTTP error message
		
#updateStock route 
@route('/updateStock/<document>', method='POST')
def update_Stock(document):
        key = request.query #retrives key from query argument
        value = request.query.result #retrives value from query argument

        if not document:
                abort(400, 'No data received')# return HTTP error message


        try:
                updateStock(key, value, document)#calls method and passes variable

        except ValidationError as ve:# return HTTP error message
                abort(400, str(ve))


#deleteStock route
@route('/deleteStock/<value>', method='DELETE')
def delete_Stock(value):

        if not value:
                abort(400, 'No data received')# return HTTP error message

        try:
                deleteStock(value)#calls method and passes variable

        except ValidationError as ve:
                abort(400, str(ve))# return HTTP error message

#stockReport Route				
@route('/stockReport/list', method='GET')
def sReport():
        list = request.query['list']

        if not list:
                abort(400, 'No data received')# return HTTP error message

        try:
                stkReport(list)#calls method and passes variable

        except ValidationError as ve:# return HTTP error message
                abort(400, str(ve))

#industryReport route
@route('/industryReport/<key>',method='GET')
def iReport (key):

        if not key:
                abort(400, 'No data received') # return HTTP error message

        try:
                indReport(key) #calls method and passes variable



if __name__ == '__main__': #declare instance of request
    #app.run(debug=True)
    run(host='0.0.0.0', port=8080) #sets adress to 0.0.0.0 & port 8080
 
