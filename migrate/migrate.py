#!/usr/bin/env python3
import logging
from pymongo import MongoClient


# Handle Config
from migrate_config import CONFIG
DB = CONFIG['db']
HOST = CONFIG['host']
PORT = CONFIG['port']
LOG_PATH = CONFIG['log']

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s:%(message)s'
)

# Database connection
client = MongoClient(HOST, PORT)
logging.info('Connected to {0}:{1} - {2}'.format(HOST, PORT, client))
db = client[DB]
logging.info('Using DB {0} - {1}'.format(DB, db))


# Actual migration scripts go below here
collection = db.user
logging.info('{0}'.format(collection))
collection.drop_indexes()
logging.info('{0}'.format(collection.index_information()))
logging.info('Dropped user indexes')
logging.info('{0}'.format(collection.index_information()))
