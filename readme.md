# Overview

This project contains demonstration scripts for the XBUS-503 Data Wrangling course at Georgetown University CCPE.  These scripts simulate the basics of a distributed ETL system using an Amazon (AWS SQS) Queue to enable multiple worker processes to transform and load data into a MongoDB store.


# Setup

There are several steps for setup of this demonstration.  The user will need to:

* Install required libraries
* Create an Amazon Web Services Account
* Download and configure AWS keys
* Create an SQS Queue
* Install MongoDB


## Install Libraries

To install the required libraries, use pip install and the provided requirements.txt file.

	pip install -r requirements.txt

## Create an Amazon Web Services account

An account for AWS can be created at [http://aws.amazon.com/](http://aws.amazon.com/).

## Download and configure security keys

The easiest way to configure your scripts for secure access will be to create an Access Key ID and Secret Access Key.  To do so visit [your account security credentials](https://console.aws.amazon.com/iam/home?#security_credential) page, open up the "Access Keys" section, and click on "Create New Access Key".  You may download the new key file depending on how you choose to supply Boto with your credentials.

It's recommended that you setup secure access to AWS according to the [Boto documentation](http://boto.readthedocs.org/en/latest/boto_config_tut.html).

## Create AWS SQS Queue

Visit the [AWS SQS](https://console.aws.amazon.com/sqs/) page to manage SQS Queues.  Click on "Create New Queue", supply a "Queue Name", and then use the provided default values.

The name you enter will need to be added to both enqueuer.py and worker.py as the value for `QUEUE_NAME`.

Note: At the time of this documentation, API requests to SQS were free up to the first one million requests per month and 50 cents per million afterwards.

## Install MongoDB

Installation documenation for MongoDB can be found of MongoDB's official website: [http://docs.mongodb.org/manual/installation/](http://docs.mongodb.org/manual/installation/).  Make sure MongoDB is running and configure `worker.py` with the correct server location, database name, and collection name as needed.

If you would like to use an alternate database, you'll need to replace [PyMongo](http://api.mongodb.org/python/current/) with the database adapter of your choice.  Some relational database examples are:

* [sqlite3](https://docs.python.org/2/library/sqlite3.html)
* [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)
* [psycopg2](http://initd.org/psycopg/docs/)
* [SQLAlchemy](http://docs.sqlalchemy.org/)

# enqueuer.py

This script will read in all CSV files within the `./data` directory, loop through each row, and send a JSON version to the SQS queue.  To activate the script, use the following command:

	python enqueuer.py

Do not attempt to run multiple copies of the `enqueuer.py` file concurrently.

# worker.py

This script will download one message at a time from the SQS Queue, transform the JSON data, and then save it to MongoDB.  To activate the script, use the following command:

	python worker.py

For an accurate demonstration you will want to run multiple copies of this script concurrently.
