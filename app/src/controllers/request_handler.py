from flask import Response, abort
from bson import json_util
import json
from datetime import datetime
from pymongo import ReturnDocument

# import internal dependencies here
from src.models import SongModel, PodcastModel, AudiobookModel


def parse_request_data(data: dict):
    try:
        # handle content type
        if data == None:
            raise KeyError
        # unpack right params
        return (data['audioFileType'], data['audioFileMetadata'])
    except KeyError:
        abort(400, description="Bad params")


def check_datestring_and_convert_to_datetime(datestring: str):
    upload_date = datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S.%f")
    if upload_date.date() < datetime.now().date():
        abort(400, description="upload date is in the past")
    return upload_date


def validate_metadata(audioFileType: str, audioFileMetadata: dict):
    if audioFileType == "song":
        return SongModel.validate(audioFileMetadata)
    elif audioFileType == "podcast":
        return PodcastModel.validate(audioFileMetadata)
    elif audioFileType == "audiobook":
        return AudiobookModel.validate(audioFileMetadata)
    else:
        abort(500, description="Not implemented.")


def create(db, data: dict):
    audioFileType, audioFileMetadata = parse_request_data(data)
  
    collection_types = db.list_collection_names()
    if audioFileType in collection_types:
        # check if date is in past and abort if so or convert to Date
        try:
            audioFileMetadata["uploaded_time"] = check_datestring_and_convert_to_datetime(audioFileMetadata["uploaded_time"])
        except KeyError:
            abort(400, description="bad metadata")
        
        # model validation
        metadata_is_valid = validate_metadata(audioFileType, audioFileMetadata)
        if not metadata_is_valid:
            abort(400, description="bad metadata")
        
        # generate new id
        last_index = list(db[audioFileType].find({}).sort("_id", -1))[0]["_id"]
        audioFileMetadata["_id"] = last_index + 1

        # fetch records to check if id exists
        record = list(db[audioFileType].find({"_id": audioFileMetadata["_id"]}))
        if record == []:
            # does not exist therefore create
            new_record_id = db[audioFileType].insert_one(audioFileMetadata).inserted_id
            res = json.dumps(
                {"new_record": list(db[audioFileType].find({"_id": new_record_id}))},
                default=json_util.default)
        else:
            abort(400, description="bad metadata")
    else:
        abort(400, description=f"{audioFileType} is not a collection")

    return Response(response=res, status=200, mimetype="application/json")


def read(db, audioFileType: str =None, audioFileID: int =None):
    collection_types = db.list_collection_names()
    
    if (audioFileType == None) and (audioFileID == None):
        # i.e. the request was send to "/"
        res = json.dumps({"audioFileTypes": collection_types})
    elif (audioFileType != None) and (audioFileID == None):
        # i.e. request was sent to "/<type>"
        if audioFileType in collection_types:
            record_list = list(db[audioFileType].find({}))
            
            res = json.dumps(
                {audioFileType: record_list}, 
                default=json_util.default)
        else:
            abort(400, description="Bad url")
    elif (audioFileType != None) and (audioFileID != None):
        # i.e. request was sent to "/<type>/<id>"
        if audioFileType in collection_types:
            record = list(db[audioFileType].find({"_id": audioFileID}))
            
            if record == []:
                abort(500, description="Record not found.")
            
            res = json.dumps(record, default=json_util.default)
        else:
            abort(400, description="Bad url")
    
    return Response(response=res, status=200, mimetype="application/json")


def update(db, data: dict, audioFileType: str, audioFileID: int):
    _, audioFileMetadata = parse_request_data(data)

    try:
        audioFileMetadata["uploaded_time"] = check_datestring_and_convert_to_datetime(audioFileMetadata["uploaded_time"])
    except KeyError:
        pass

    collection_types = db.list_collection_names()
    if audioFileType in collection_types:
        updated_record = db[audioFileType].find_one_and_update(
            {"_id": audioFileID},
            {"$set": audioFileMetadata},
            return_document=ReturnDocument.AFTER)
        
        if updated_record == None:
            abort(500, description="Cannot update user. Something went wrong.")
        
        res = json.dumps(
            {"updated_record": updated_record},
            default=json_util.default)
    else:
        abort(400, description="Bad url")
        
    return Response(response=res, status=200, mimetype="application/json")


def delete(db, audioFileType: str, audioFileID: int):
    collection_types = db.list_collection_names()
    
    if audioFileType in collection_types:
        delete_count = db[audioFileType].delete_one({"_id": audioFileID}).deleted_count
        res = json.dumps({"deleted": delete_count}, default=json_util.default)
    else:
        abort(400, description="Bad url")
    
    return Response(response=res, status=200, mimetype="application/json")
