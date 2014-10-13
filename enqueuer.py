# enqueuer.py
# Enqueues data from CSVs to AWS SQS
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
# ID: enqueuer.py [] allen.leis@gmail.com

"""
Process CSVs and adds each row to an AWS SQS Queue as a Dictionary object
"""

##########################################################################
## Imports
##########################################################################

import os
import boto.sqs
import unicodecsv
import json
import sys

from os.path import basename
from time import sleep
from boto.sqs.message import Message

##########################################################################
## CONSTANTS
##########################################################################

QUEUE_NAME = 'data-wrangling-course'
DATA_PATH = './data'


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

def get_files():
    '''
    convenience function to return a list of paths to all files with a 
    .csv extension in the data subdirectory
    '''
    file_extension_mask = 'csv'
    return [os.path.join('.','data', f) for f in os.listdir(DATA_PATH) 
        if f.endswith(file_extension_mask)]


##########################################################################
## Main Functions
##########################################################################


def enqueue(queue, files):
    '''
    loops through an array of CSV file paths in order to convert each row
    to a JSON object, and then add it to the SQS Queue
    '''    
    counter = 0
    for f in files:
        symbol = os.path.splitext(basename(f))[0]
        reader = unicodecsv.DictReader(open(f))
        for data in reader:
            data['symbol'] = symbol
            package = json.dumps(data)

            m = Message()
            m.set_body(package)
            queue.write(m)
            counter += 1
            ping()
    print "\n\nExiting - End of data files.  %d rows queued.\n" % counter


##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    queue = get_queue()
    files = get_files()
    enqueue(queue, files)

