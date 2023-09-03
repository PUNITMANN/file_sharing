import traceback
import logging
import uuid

from helpers.my_sql_connector import my_sql_execute_query
from signup_api.utils import check_email_validation, generate_api_key
from email_verifiy.email_verify import send_email


def sign_up(data):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        email = data.get("email", "")
        password = data.get("password", "")
        re_enter_password = data.get("re_enter_password", "")
        user_type = data.get("user_type", "")
        verify_code = str(uuid.uuid4())[:6]

        if not email:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Email must not be empty"})
            return response
        if not password or not re_enter_password:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Both Password must not be empty"})
            return response

        if password != re_enter_password:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Both Password must be same"})
            return response

        if not user_type:
            response.update({"status": "Bad Request", "status_code": 400, "message": "user_type must not be empty"})
            return response

        if user_type not in ["operation_user", "client_user"]:
            response.update({"status": "Bad Request", "status_code": 400, "message": "user_type must be operation_type or client_type only"})
            return response

        email_valid = check_email_validation(email)
        if not email_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Email Format"})
            return response

        query = "select * from auth_user;"
        results, status_code = my_sql_execute_query(query)
        if status_code == 500:
            return response
        if status_code == 200:
            email_exists = any(item[1] == email for item in results)
            if email_exists:
                response.update({"status": "Bad Request", "status_code": 400, "message": "Email Already Exists"})
                return response
        if user_type == "operation_user":    # by default operational user is verified
            verify_code = 0
            is_verified = 1
        else:
            is_verified = 0

        result = generate_api_key()
        if result.get("status_code") == 500:
            return result
        x_api_key = result.get("secret_key")
        query2 = f"insert into auth_user (email, password, created_at, x_api_key, user_type, verify_code, is_verified) VALUES ('{email}', '{password}', NOW(), '{x_api_key}', '{user_type}', '{verify_code}', '{is_verified}');"
        results, status_code = my_sql_execute_query(query2)
        if status_code == 500:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Error in Inserting Data into Database"})
            return response
        if status_code == 200 and user_type == "client_user":
            email_sended = send_email(verify_code, email, user_type)
            if email_sended.get("status_code") == 200:
                response.update({"status": "Success", "status_code": 200, "message": f"User with email {email} signed up successfully", "x_api_key": x_api_key})
                return response
            else:
                query3 = f"delete from auth_user where email = {email};"
                results, status_code = my_sql_execute_query(query3)
                response.update({"status": "failure", "status_code": 400,
                                 "message": f"User with email {email} does not signed up successfully"})
                return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
        return response
