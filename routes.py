from flask import Flask, redirect, url_for, render_template, request, jsonify
import boto3
from application import application
import dynamoDBHandler as dynamodb

# index page route

@application.route('/')
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
    items = dynamodb.displayCustomers()
   # sorted(items, key = lambda i: i['CustomerId'])
    #print(sorted(dicts, key = lambda item: item['salary']))
    items1 = sorted(items, key=itemgetter('CustomerId'))
    
    return render_template('display.html', items = items1)



# search page 
@application.route("/search", methods= ['GET', 'POST'])
def search():
    
    if request.method == 'POST':
        searchName = request.form['name']
        
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

        if name != "" :
            
            #if newitem['name'] == "" and newitem['address'] == "" and newitem['city'] == "" and newitem['state'] == "" and newitem['phone'] == "" :

            if not any(newitem.values()):
                return render_template("edit.html", noeditmsg = 1, name = name)
            else :
                success = 5
                response, itemfound = dynamodb.searchCustomer(name)
                if itemfound == 1 :
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
    response = dynamodb.getCustomerbyId(id)
    item = response['Item']
    # print(item)
    return render_template('get.html', item = item)


#delete page
@application.route("/delete/", methods = ['GET', 'POST'] )
def delete():
    if request.method == 'POST':
        delName = request.form['name']
        
        if delName :
            response = dynamodb.delCustomer(delName)
            if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                return render_template("del.html", delName = delName, success = 1 )
            else:
                return render_template("del.html", delName = delName, response = response, success = 0)
           
        else :
            return render_template("del.html", nonamemsg = 1)
                    
    return render_template("del.html", delName = "delete customer")


'''
@application.route('/get')
def get():
    table = dynamodb.Table('YourTestTable')
    response = table.get_item(
        Key={
            'Name': 'Anju',
            'Department': 'Manager'
        }
    )
    item = response['Item']
    # print(item)
    return render_template('get.html', item = item)

@application.route('/update')
def update():
    table = dynamodb.Table('YourTestTable')
    table.update_item(
        Key={
            'Name': 'Zee',
            'Department': 'AWS'
        },
        AttributeUpdates={
            'Department': {
                'Value'  : 'aws' ,
                'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
            }
        }
    )


'''