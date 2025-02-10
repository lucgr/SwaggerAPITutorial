import json
import logging
import os
import tempfile
import uuid
from functools import reduce

from pymongo import MongoClient

from swagger_server.models import Student

mongo_db_client = MongoClient("mongodb://mongo:27017")
student_db = mongo_db_client["student_database"]
student_collection = student_db["students"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add(student=None):
    res = student_collection.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })
    if res:
        return 'already exists', 409

    student_dict = student.to_dict()
    student_dict['uid'] = str(uuid.uuid4())

    doc_id = student_collection.insert_one(student_dict)

    return student_dict['uid'], 200


def get_by_id(student_id=None, subject=None):
    student_response = student_collection.find_one({"uid": student_id})
    if not student_response:
        return 'not found', 404

    logger.info(f"Student response from DB: {student_response}")
    student_dict = student_response_to_student(student_response)
    logger.info(f"Processed student dict: {student_dict}")

    return student_response_to_student(student_response), 200, [("Content-Type", "application/json")]


def delete(student_id=None):
    student = student_collection.find_one({"uid": student_id})
    if not student:
        return 'not found', 404
    student_collection.delete_one(student)
    return student_id, 200

def student_response_to_student(student_response):
    student = Student(
        student_id=student_response['student_id'],
        first_name=student_response['first_name'],
        last_name=student_response['last_name'],
        grade_records=student_response['grade_records'] if student_response['grade_records'] is not None else []
    )
    return student
