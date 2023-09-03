import traceback
import logging
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from helpers.my_sql_connector import my_sql_execute_query


def send_email(verify_code, email_send_to, user_type):
    response = {"status": "failure", "status_code": 500}
    MY_EMAIL = "punitmann9599@gmail.com"
    PASSWORD = "noklwrojhlvdhzgr"
    TO_EMAIL = email_send_to

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = "Email Verification for File Sharing"

    verification_data = {
        "verify_code": verify_code,
        "user_type": user_type,
        "email": email_send_to
    }

    # Convert the dictionary to a JSON-formatted string
    json_data = json.dumps(verification_data, indent=4)

    # Add the message body
    body = f"Use this Verify Code for Verification: {verify_code} and user_type: client_user also use this curl to verify \n"
    body += f"curl --location --request PUT 'http://127.0.0.1:8000/verify_user' "
    body += f" and add this into the body '{json_data}'"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
        response = {"status": "success", "status_code": 200}
        return response
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


def verify_user(data):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        email = data.get("email", "")
        user_type = data.get("user_type", "")
        verify_code = data.get("verify_code", "")

        if not email:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Email must not be empty"})
            return response

        if not user_type:
            response.update({"status": "Bad Request", "status_code": 400, "message": "user_type must not be empty"})
            return response

        if user_type == "operation_user":
            response.update({"status": "Bad Request", "status_code": 400, "message": "user_type must be client_type only for verification"})
            return response

        if not verify_code:
            response.update({"status": "Bad Request", "status_code": 400, "message": "verify_code must not be empty"})
            return response

        query = f"select * from auth_user where email = '{email}'"
        result, status_code = my_sql_execute_query(query)
        if status_code == 500:
            return response
        if status_code == 200:
            if result[0][8] == verify_code:

                query2 = f"update auth_user set is_verified = 1 where email = '{email}';"
                results, status_code = my_sql_execute_query(query2)
                if status_code == 500:
                    response.update({"status": "Bad Request", "status_code": 400, "message": "Error in Updating Data into Database"})
                    return response
                if status_code == 200:
                    response.update({"status": "Success", "status_code": 200, "message": f"User with email {email} Verified successfully"})
                    return response
            else:
                response.update({"status": "Bad Request", "status_code": 400, "message": "Verified Code doesn't match"})
                return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
        return response
