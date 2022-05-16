'''
Author - Zahida Meeran
Date - 5/12/2022
Reference : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

'''


from urllib import response
import boto3
from boto3.dynamodb.conditions import Key, Attr
#from requests import Response


'''
dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY)
   #                region_name ='us-east-1')


'''

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
dynamo_client = boto3.client('dynamodb', region_name = 'us-east-1')

# Create the customers table in DynamoDB 

def createCustomersTable():
    table = dynamodb.create_table(
        TableName='customers',
        KeySchema=[
            {
                'AttributeName': 'CustomerId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'CustomerId',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.wait_until_exists()

    # Print out some data about the table.
    print(table.item_count)

table= dynamodb.Table('customers')


def displayCustomers():

    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    return data


# search function that queries the dynamo db table 'customers' searching for a customer name

def searchCustomer(name):
    response = table.scan(FilterExpression=Attr('Name').eq(name))
    data = response['Items']
    count = len(data)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return data, count

    return response, count



# add new customer record/item  to the customers table in dynamodb

def addCustomer(name, address, city, state, ph):
    # reading the items and getting the customerid and finding the maximum one to auto increment the id
    # auto increment not supported in dynamodb

    response = table.scan()
    idlist = response['Items']
    ids = []
    for i in idlist:
        ids.append(i['CustomerId'])

    id = max(ids) + 1

    response = table.put_item(
        Item = {
            'CustomerId' : id,
            'Name'  : name,
            'Address' : address,
            'City'  : city,
            'State' : state,
            'Phone' : ph
        }
    )
    return response

# get the a particular customer using id
def getCustomerbyId(id):
    response = table.get_item(
        Key={
            'CustomerId': id,
        }
    )
    return response
    

def editCustomer(id, item):
    statuscode = 200
    if item['name']:
        response = table.update_item(
            Key = {
                'CustomerId': id
            },
            AttributeUpdates={
                'Name': {
                    'Value'  : item['name'],
                    'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
                }
            },
            ReturnValues = "UPDATED_NEW"  # returns the new updated values
        )
        statuscode = response['ResponseMetadata']['HTTPStatusCode'] 

    if item['address'] and statuscode == 200 :
        response = table.update_item(
            Key = {
                'CustomerId': id
            },
            AttributeUpdates={
                'Address': {
                    'Value'  : item['address'],
                    'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
                }
            },
            ReturnValues = "UPDATED_NEW"  # returns the new updated values
        )
        statuscode = response['ResponseMetadata']['HTTPStatusCode'] 
    
    if item['city'] and statuscode == 200 :
        response = table.update_item(
            Key = {
                'CustomerId': id
            },
            AttributeUpdates={
                'City': {
                    'Value'  : item['city'],
                    'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
                }
            },
            ReturnValues = "UPDATED_NEW"  # returns the new updated values
        )
        statuscode = response['ResponseMetadata']['HTTPStatusCode'] 
    
    if item['state'] and statuscode == 200 :
        response = table.update_item(
            Key = {
                'CustomerId': id
            },
            AttributeUpdates={
                'State': {
                    'Value'  : item['state'],
                    'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
                }
            },
            ReturnValues = "UPDATED_NEW"  # returns the new updated values
        )
        statuscode = response['ResponseMetadata']['HTTPStatusCode'] 
    
    if item['phone'] and statuscode == 200 :
        response = table.update_item(
            Key = {
                'CustomerId': id
            },
            AttributeUpdates={
                'Phone': {
                    'Value'  : item['phone'],
                    'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
                }
            },
            ReturnValues = "UPDATED_NEW"  # returns the new updated values
        )
        
    return response



def delCustomer(name):
    response = table.scan(FilterExpression=Attr('Name').eq(name))
    data = response['Items']
    
    for i in data :
        response = table.delete_item(
            Key={
                'CustomerId': i['CustomerId'],
            }
        )
        return response



