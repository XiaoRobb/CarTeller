
import os

dbhost = 'localhost:3306'
dbuser = 'root'
dbpass = 'root'
dbname = 'flask1'
DB_URI = 'mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname

basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
