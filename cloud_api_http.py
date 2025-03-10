#!/usr/bin/env python3
import os
import yaml
import re
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Load configuration from config.yaml
try:
    configs = yaml.safe_load(open('config.yaml'))
    print("Loaded configs:", configs)
except Exception as e:
    print("Error loading config.yaml:", e)
    exit(1)

app = FastAPI()

@app.get("/login")
async def pilot_login():
    # Use your working file path (adjust if needed)
    file_path = "html/login.html"
    if not os.path.exists(file_path):
        error_msg = f"<h2>Error: File '{file_path}' does not exist.</h2>"
        print(error_msg)
        return HTMLResponse(error_msg, status_code=500)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except Exception as e:
        error_msg = f"<h2>Error reading HTML file: {e}</h2>"
        print(error_msg)
        return HTMLResponse(error_msg, status_code=500)

    # Replace placeholders with configuration values
    try:
        file_content = re.sub(
            r'const APP_ID = "?\w+"?;',
            f'const APP_ID = "{configs["dji"]["APP_ID"]}";',
            file_content
        )
        file_content = file_content.replace("dji_license_here", configs['dji']['LICENSE'])
        file_content = file_content.replace("dji_app_key_here", configs['dji']['APP_KEY'])
        file_content = file_content.replace(
            "mqtt_host_here",
            f"tcp://{configs['mqtt']['HOST']}:{configs['mqtt']['PORT']}"
        )
        file_content = file_content.replace("mqtt_connect_callback", configs['mqtt']['CONNECT_CALLBACK'])
        file_content = file_content.replace("mqtt_username_here", configs['mqtt']['USERNAME'])
        file_content = file_content.replace("mqtt_password_here", configs['mqtt']['PASSWORD'])
    except Exception as e:
        error_msg = f"<h2>Error processing HTML file: {e}</h2>"
        print(error_msg)
        return HTMLResponse(error_msg, status_code=500)

    print(f"Modified HTML served from {file_path}")
    return HTMLResponse(file_content)

if __name__ == "__main__":
    uvicorn.run(app, host=configs['fastAPI']['HOST'], port=configs['fastAPI']['PORT'])
