__author__ = "Sandeepan B <bsandeepan95.work@gmail.com>"

from flask import Flask, request, Response, abort, jsonify

# import db orm here 
from src.db import connect_to_mongodb

# import internal dependencies here
from src.app_config import get_app_vars
from src.controllers import request_handler

def create_app():
    # instantiate app
    app = Flask(__name__)

    # configure_app
    app_vars = get_app_vars()

    #connect to db
    DB_URI = app_vars["DB_URI"]
    DB_NAME = app_vars["DB_NAME"]
    mongo = connect_to_mongodb(DB_URI)
    db = mongo[DB_NAME]

    # define routes
    @app.route("/", methods=["GET", "POST"])
    def app_create_records_or_get_audioFileTypes():
        if request.method == "GET":
            return request_handler.read(db)
        elif request.method == "POST":
            return request_handler.create(db, request.get_json())
    
            
    @app.route("/<string:audioFileType>", methods=["GET",])
    def app_get_audioFiles(audioFileType=None):
        return request_handler.read(db, audioFileType)
        

    @app.route("/<string:audioFileType>/<int:audioFileID>", methods=["GET", "PUT", "DELETE"])
    def app_handle_crud(audioFileType=None, audioFileID=None):
        if request.method == "GET":
            return request_handler.read(db, audioFileType, audioFileID)
        elif request.method == "PUT":
            return request_handler.update(db, request.get_json(), audioFileType, audioFileID)
        elif request.method == "DELETE":
            return request_handler.delete(db, audioFileType, audioFileID)


    # Error Handlers
    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify(status=500, message=str(e)), 500
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify(status=400, message=str(e)), 400
    
    return app