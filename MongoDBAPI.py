!/usr/bin/python

import json
import bottle

#Library Imports
from bson import json_util
from bottle import route, run, request, abort, post, get, put, delete
from pymongo import MongoClient

#Initializes address variables for accesssing Database & Client
client = MongoClient('localhost', 27017)
db = client.market
collection = db.stocks

#Check Username and password credentials prior to login to Database. 
def c_login(u,p):
    if username in usernames and password in username.password:
         return True
     else:
         return False
		 
# Creates new Document, returns html 400 code as exception if failed
def createStock(document): 
	try:
		result = collection.save(document)
		
	except ValidationError as ve:
		abort(400, str(ve))
			
	return result

#Reads exsisting document, returns html 404 code as exception if failed	
def readStock(value):
	result = collection.find_one({ 'Ticker' : value})
		
	if not result:
		abort(404, 'No document with TICKER %s found' % value)
	return (result)

#Reads exsisting document, returns html 404 code as exception if failed	
def updateStock(key, value, document):
	post_input = collection.update({'Ticker': document}, {'$set':{key: value}}, upsert=False, multi=False)
		
	if not result:
		abort(404, 'No document with %s : %s' % key, value)

	return json.loads(json.dumps(result, indent=4, default=json_util.default))


# Deletes exsisting document, returns html 404 code as exception if failed	
def delete_document(key, value): 
    result = collection.remove({key:value}) 

    if not result: 

        abort(404, 'No document with %s : %s' % key,value) 

    return result 

#API route call to Check credentials to Mongo CLient	
@route('/login', method='POST')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if c_login(username, password) is True:
        return "Welcome"
    else:
        return "Username or Password Incorrect"


#API route call to initialize loging form in browser	
@route('/login')
def log_in():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        form>
	'''

#API call to create new document in Mongo Database	
@route('/create', method='POST') 
def put_document():
    data = request.body.readline() 
    if not data:
         abort(400, 'No data received') 
		entity = json.loads(data)
    if not entity.has_key('id'):
         abort(400, 'No id specified') 
    try:
        createStockt(entity) 
    except ValidationError as ve:
        abort(400, str(ve))

#API call to read database and return stock document using ID identifier		
@get('/getStock/<document>')
def get_Stock(document):
	        
	if not ticker:
		abort(400, 'No data received')
		
	try:
		readStock(document)
		
	except ValidationError as ve:
		abort(400, str(ve)) 

#API call to update Mongo document using ID identifier
@put('/updateStock/<document>/')
def update():
      old_doc = get_document("id",request.query.id) 

      entity=update_document(request.query.id,request.query.result,old_doc) 

      if not entity: 

             abort(404, 'update error %s' % request.query.result)
      return json.loads(json.dumps(entity, indent=4, default=json_util.default))

#API call to delete Mongo document using ID identifier
@route('/delete', method='GET') 
def delete_document(): 

        entity=delete_document("id",request.query.id) 

        if not entity: 

                  abort(404, 'delete error %s' % request.query.id)
        return json.loads(json.dumps(entity, indent=4, default=json_util.default)) 

#API call return MongoDB document using Ticker field		
@route('/stocks/api/v1.0/stockReport', method='POST')
def getReport():
		read_result = []
	for tickerSymbol in request.json.list:
		read_result.append(read_document({"Ticker": tickerSymbol}))
	print(read_result)

	if(isinstance(read_result, Exception)):
		print('exeption')
		abort(500, "Database Error")

	return json.dumps(read_result, sort_keys=True, indent=4, default=json_util.default)
	
#API call return MongoDB documents Matching Industry Field
@route('/stocks/api/v1.0/industryReport/<industry>', method='GET')
def portfolio(industry = None): 
	
	try: 
		pipeLine = [{"$match":{"Industry":industry}},{"$project":{
		"Company":1,"Price":1}},{"$sort":{"Price":-1}},{"$limit":5}]

		stockResults = list(db.stocks.aggregate(pipeLine))
	
		return json.dumps(stockResults, indent=4, default=json_util.default) 

	except NameError:
		abort(404, 'No parameter for id %s' % id)

#Initializes address of MongoDB Client
if __name__ == '__main__': 
    app.run(debug=True)
    run(host='localhost', port=8080)