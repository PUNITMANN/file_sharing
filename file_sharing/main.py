import logging
import traceback
import os
from fastapi import FastAPI, Request, Path, HTTPException, Depends, UploadFile
from typing import List, Dict


from signup_api.signup import sign_up
from login_api.login import log_in
from signup_api.utils import generate_api_key
from authorizer.authorizer import token_required
from upload_file.upload_file import upload_file, upload_file_lists
from email_verifiy.email_verify import verify_user
from download_file.download_file import download_file


app = FastAPI()



@app.post("/signup")
@app.post("/signup/")
async def signup_api(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        data = await request.json()
        response = sign_up(data)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.post("/login")
@app.post("/login/")
async def login_api(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        data = await request.json()
        response = log_in(data)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.get("/create_x_api_key")
@app.get("/create_x_api_key/")
async def create_x_api_key(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        response = generate_api_key()
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.post("/upload_file")
@app.post("/upload_file/")
@token_required
async def upload_file_api(request: Request, file: UploadFile):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        user_id_payload = request.state.user_id
        user_id = user_id_payload.get("user_id")
        user_type_payload = request.state.user_type
        user_type = user_type_payload.get("user_type")

        response = upload_file(user_id, user_type, file)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.put("/verify_user")
@app.put("/verify_user/")
async def verifying_user(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        data = await request.json()
        response = verify_user(data)
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.post("/download_file")
@app.post("/download_file/{secret_code}")
@app.post("/download_file/{secret_code}/")
@token_required
async def download_file_api(request: Request, secret_code: str = None):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        user_type_payload = request.state.user_type
        user_type = user_type_payload.get("user_type")

        response = download_file(user_type, secret_code)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.get("/upload_file_list")
@app.get("/upload_file_list/")
@token_required
async def upload_file_list(request: Request, secret_code: str = None):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        user_id_payload = request.state.user_id
        user_id = user_id_payload.get("user_id")

        response = upload_file_lists(user_id)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response

