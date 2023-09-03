import os
import logging
import traceback
import uuid

from flask import Flask, request  # You'll need Flask for this

app = Flask(__name__)

from helpers.my_sql_connector import my_sql_execute_query

UPLOAD_DIR = "/Users/Punit/Documents/upload_server"
FILE_ALLOWED = [".pptx", ".docx", ".xlsx"]


def download_file(user_type, secret_code):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        if not secret_code:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Secret Code must be Present"})
            return response
        if user_type == "operation_user":
            response.update({"status": "Bad Request", "status_code": 400, "message": "operational user are not allowed to Download the file"})
            return response

        query = f"select * from file_sharing where secret_code = '{secret_code}'"
        result, status_code = my_sql_execute_query(query)
        if not result:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Secret Code"})
            return response
        file_name = result[0][1]+result[0][4]
        file_path = os.path.join(UPLOAD_DIR, file_name)

        # Check if the file exists at the specified path
        if not os.path.exists(file_path):
            response.update({"status": "Failure", "status_code": 400, "message": "File not found"})
            return response

        # Open and read the file
        with open(file_path, "rb") as f:
            file_content = f.read()

        download_folder = os.path.expanduser("~/Downloads")  # User's home directory
        download_path = os.path.join(download_folder, file_name)

        with open(download_path, "wb") as f:
            f.write(file_content)
        response.update({"status": "Success", "status_code": 200, "message": "File Downloaded Successfully Please check Download Folder"})
        return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response
