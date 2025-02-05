import os
import tempfile
from functools import reduce

# from tinydb import TinyDB, Query
from pymongo import MongoClient

# TODO: delete
# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

mongo_db_client = MongoClient("mongodb://mongo:27017")
student_db = mongo_db_client["student_database"]
student_collection = student_db["students"]

def add(student=None):
    res = student_collection.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })
    if res:
        return 'already exists', 409

    doc_id = student_collection.insert_one(student.to_dict())
    # student.student_id = int(str(doc_id.inserted_id))
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_collection.find_one({"student_id": int(student_id)})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = student_collection.find_one({"student_id": int(student_id)})
    if not student:
        return 'not found', 404
    student_collection.delete_one(student)
    return student_id