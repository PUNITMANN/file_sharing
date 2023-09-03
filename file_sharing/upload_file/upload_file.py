import os
import logging
import traceback
import uuid

from helpers.my_sql_connector import my_sql_execute_query

UPLOAD_DIR = "/Users/Punit/Documents/upload_server"
FILE_ALLOWED = [".pptx", ".docx", ".xlsx"]


def upload_file(user_id, user_type, file):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        secret_code = str(uuid.uuid4())[:6]
        filename, file_extension = os.path.splitext(file.filename)
        if not file:
            response.update({"status": "Bad Request", "status_code": 400, "message": f"File must be Present"})
            return response

        if user_type == "client_user":
            response.update({"status": "Bad Request", "status_code": 400, "message": "Client user are not allowed to Upload the file"})
            return response

        if file_extension not in FILE_ALLOWED:
            response.update({"status": "Bad Request", "status_code": 400, "message": f"File Type must be from {FILE_ALLOWED}"})
            return response

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        query = f"insert into file_sharing (user_id, file_name, uploaded_at, file_extension, secret_code) VALUES ('{user_id}','{filename}', NOW(), '{file_extension}', '{secret_code}')"
        results, status_code = my_sql_execute_query(query)
        if status_code == 500:
            response.update(
                {"status": "Bad Request", "status_code": 400, "message": "Error in Inserting Data into Database"})
            return response
        if status_code == 200:
            response.update({"status": "Success", "status_code": 200, "message": "file uploaded successfully", "secret_code": f"Use this secret code {secret_code} to Share and Download the File"})
            return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


def upload_file_lists(user_id):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:

        data = []
        query = f"select * from file_sharing where user_id = '{user_id}'"
        results, status_code = my_sql_execute_query(query)
        if status_code == 500:
            response.update(
                {"status": "Bad Request", "status_code": 400, "message": "Error in Fetching Data from the Database"})
            return response
        for result in results:
            file_name = result[1] + result[4]
            uploaded_at = result[3]
            secret_code = result[5]
            raw_data = {"file_name": file_name, "secret_code": secret_code, "uploaded_at": uploaded_at}
            data.append(raw_data)

        response.update({"status": "Success", "status_code": 200, "message": "Data Fetched Successfully", "data": data})
        return response
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response
