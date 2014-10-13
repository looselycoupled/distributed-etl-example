# Overview

This project contains demonstration scripts for the XBUS-503 Data Wrangling course at Georgetown University.  These scripts simulate the basics of a distributed ETL system using an Amazon (AWS SQS) Queue to enable multiple worker processes to transform and load data into a MongoDB store.

This readme assumes that you 

# Setup

There are three primary concerns for setup of this demonstration.  The user will need to:

* Install required libraries
* Create an Amazon Web Services Account
* Download and configure AWS keys
* Create an SQS Queue
* Configure worker.py with the database and collection name

## Install Libraries

To install the required libraries, use pip install and the provided requirements.txt file.

	pip install -r requirements.txt
	
## Create an Amazon Web Services account

An account can be created [http://aws.amazon.com/](http://aws.amazon.com/).

## Download and configure security keys

The easiest way to configure your scripts for secure access will be to create an Access Key ID and Secret Access Key.  To do so visit [your account security credentials](https://console.aws.amazon.com/iam/home?#security_credential) page, open up the "Access Keys" section, and click on "Create New Access Key".  You may download the new key file depending on how you choose to supply Boto with your credentials.

It's recommended that you setup secure access to AWS according to the [Boto documentation](http://boto.readthedocs.org/en/latest/boto_config_tut.html).

## Create AWS SQS Queue

Visit the [AWS SQS](https://console.aws.amazon.com/sqs/) page to manage SQS Queues.  Click on "Create New Queue", supply a "Queue Name", and then use the provided default values.

The name you entered will need to be added to both enqueuer.py and worker.py as the value for `QUEUE_NAME`.