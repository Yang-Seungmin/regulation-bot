from peewee import MySQLDatabase
from bot.regulation_secrets import *

db = MySQLDatabase(db_name, host=db_host, port=db_port, user=db_user, password=db_password)
