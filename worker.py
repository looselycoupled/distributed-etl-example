# worker.py
# Transforms messages from an AWS SQS Queue and loads them into a 
# MongoDB database
#
# In order to run, you will need an AWS account and have added your
# access and secret keys to your environmental variables or boto 
# config as detailed in the boto documentation.
# 
# Note that this is for demonstration only and is not production ready 
# code.  At a minimum this file would require exeption handling, logging, 
# etc.
# 
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Wed Oct 8 20:14:08 2014 -0400
#
# ID: worker.py [] allen.leis@gmail.com

"""
Transforms messages from an AWS SQS Queue and adds to a MongoDB database
"""

##########################################################################
## Imports
##########################################################################

import boto.sqs
import json
import sys

from pymongo import MongoClient
from datetime import datetime

##########################################################################
## CONSTANTS
##########################################################################

QUEUE_NAME = 'data-wrangling-course'
CONNECTION_STRING = 'mongodb://localhost:27017/'
DB_NAME='financials'
COLLECTION_NAME='summaries'


##########################################################################
## Helper Functions
##########################################################################

def ping():
    '''
    simple function to draw a dot to the screen every time a message is
    processed
    '''
    sys.stdout.write('.')
    sys.stdout.flush()

def get_queue():
    '''
    convenience function to return a connection to the SQS Queue
    '''
    conn = boto.sqs.connect_to_region("us-east-1")
    return conn.get_queue(QUEUE_NAME)

def get_collection():
    '''
    convenience function to return a pymongo collection object in order
    to add new documents
    '''
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


##########################################################################
## Main Functions
##########################################################################

def transform(data):
    '''
    Accepts a Dictionary and then transforms the data according 
    to the following:

      - remove Adjusted Close
      - convert Date from String datetime data type
      - convert numeric String values to int representations
      - uppercase the symbol
      - compute the average price from the high and low

    '''
    return {
        'symbol' : data['symbol'].upper(),
        'date' : datetime.strptime(data['Date'], '%Y-%m-%d'),
        'data' : {
            'open' : int(float(data['Open']) * 100),
            'high' : int(float(data['High']) * 100),
            'low' : int(float(data['Low']) * 100),
            'close' : int(float(data['Close']) * 100),
            'volume' : int(float(data['Volume'])),
            'average' : int( ( (float(data['High']) + float(data['Low'])) / 2 ) * 100 ),
        }
    }


def work(queue, collection):
    '''
    loops through an SQS Queue, transforms each message, and loads it into
    a MongoDB database.
    '''
    counter = 0
    while True:
        m = queue.read()
        if m == None:
            print "\nExiting - End of Queue reached.  %d messages processed." % counter
            break
        data = json.loads(m.get_body())
        collection.insert(transform(data))
        res = queue.delete_message(m)
        counter += 1
        ping()


##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    queue = get_queue()
    collection = get_collection()
    work(queue, collection)    



