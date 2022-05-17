'''
Author - Zahida Meeran
Date - 5/12/2022

This is the routing script 

'''



from flask import Flask, redirect, url_for, render_template, request, jsonify
import boto3
from application import application
import dynamoDBHandler as dynamodb

# index page route

@application.route('/')
@application.route('/home')
def index():
    return render_template('index.html')


# add (customer) page
@application.route('/add/', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        
        # if name is given, addCustomer function (from dynamoDBHandler.py)  is called 
        if name != "" :
            response = dynamodb.addCustomer(name, address, city, state, phone)  
            if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                success = True
                return render_template("add.html", name = name, success = success)
            else:
                return {  
                    'msg': 'Some error occcured',
                    'response': response
                }
        else :
            return render_template("add.html", nonamemsg = 1 )
            
    return render_template("add.html")


# display page
@application.route("/display/", methods= ['GET'])
def display():
    from operator import itemgetter

    # displayCustomer function (from dynamoDBHandler.py)  is called 
    # to get the items/records from the dynamoDB table and stored in items which is a list of dictionaries
    items = dynamodb.displayCustomers()
    
    # sorting the dictionaries(records or items in the table) by CustomerId in the items list
    # and storing in items1 list

    # sorting the items list with key value CustomerId in the dictitonaries using lambda function or itemgetter
    # sorted(items, key = lambda i: i['CustomerId']) 
    
    items1 = sorted(items, key=itemgetter('CustomerId'))
    
    return render_template('display.html', items = items1)



# search page 
@application.route("/search", methods= ['GET', 'POST'])
def search():
    
    if request.method == 'POST':
        searchName = request.form['name']
        
        # calling searchCustomer function from dynamoDBHandler.py, it returns the list of items and count of items

        if searchName:                        
            items, count = dynamodb.searchCustomer(searchName)
            return render_template("search.html", searchName = searchName, count = count, items = items )
           
        else :
            return render_template("search.html", nonamemsg = 1, count = -1)
        
    return render_template("search.html", searchName = "Search Name", count = -1)



# edit page
@application.route("/edit", methods = ['GET', 'POST'])
def edit():
    newitem = { 
                'name': '',
                'address': '',
                'city' : '',
                'state' : '',
                'phone' : ''
        }

    if request.method == 'POST':
        name = request.form['name']
        newitem['name'] = request.form['newname'] 
        newitem['address'] = request.form['address']
        newitem['city'] = request.form['city']
        newitem['state'] = request.form['state']
        newitem['phone'] = request.form['phone']
        #editdetails = 0

        if name != "" :
                      
            #if newitem['name'] == "" and newitem['address'] == "" and newitem['city'] == "" and newitem['state'] == "" and newitem['phone'] == "" :

            if not any(newitem.values()):
                return render_template("edit.html", noeditmsg = 1, name = name)
            else :
                success = 5
                
                # calling searchCustomer function from dynamoDBHandler.py to search the table for the given name

                response, itemfound = dynamodb.searchCustomer(name)
                if itemfound == 1 :

                   # response = dynamodb.editCustomer(response[0]['CustomerId'], newitem)
                    response = dynamodb.editCustomer(response[0]['CustomerId'], newitem)   
                    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                        success = 1
                    else :
                        success = 0
                return render_template('edit.html', success = success, name = name, itemfound = itemfound, response = response)
        else :
            return render_template("edit.html", name = "Edit Customer Name", nonamemsg = 1)

    return render_template("edit.html", name = "Edit Customer Name")



# get page using id
@application.route('/get/<int:id>')
def get(id):

    # calling getCustomerId function from dynamoDBHandler.py to get a particular item based on id entered

    response = dynamodb.getCustomerbyId(id)
    item = response['Item']
    # print(item)
    return render_template('get.html', item = item)



#delete page
@application.route("/delete/", methods = ['GET', 'POST'] )
def delete():
    if request.method == 'POST':
        delName = request.form['name']
        
        # calling delCustomer function from dynamoDBHandler.py to del an item/record from table 
                    
        if delName :
            response = dynamodb.delCustomer(delName)
            if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                return render_template("del.html", delName = delName, success = 1 )
            else:
                return render_template("del.html", delName = delName, response = response, success = 0)
           
        else :
            return render_template("del.html", nonamemsg = 1)
                    
    return render_template("del.html", delName = "delete customer")