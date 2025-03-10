#!/usr/bin/env python3
import os
import yaml
import re

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

configs = yaml.safe_load(open('config.yaml'))
print(configs)

app = FastAPI()


@app.get("/login")
async def pilot_login():
    file_path = "./couldhtml/login.html"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        file_content = re.sub(r'const APP_ID = "?\w+"?;', f'const APP_ID = "{configs["dji"]["APP_ID"]}";', file_content)
        file_content = file_content.replace("dji_license_here", configs['dji']['LICENSE'])
        file_content = file_content.replace("dji_app_key_here", configs['dji']['APP_KEY'])
        file_content = file_content.replace("mqtt_host_here",
                                            f"tcp://{configs['mqtt']['HOST']}:{configs['mqtt']['PORT']}")
        file_content = file_content.replace("mqtt_connect_callback", configs['mqtt']['CONNECT_CALLBACK'])
        file_content = file_content.replace("mqtt_username_here", configs['mqtt']['USERNAME'])
        file_content = file_content.replace("mqtt_password_here", configs['mqtt']['PASSWORD'])

        # file_content.replace("hostnamehere", host_addr)
        # file_content.replace("userloginhere", username)
        # file_content.replace("userpasswordhere", password)
        # Overwrite the original file to ensure changes persist
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(file_content)
        #
        print(f"Modified HTML saved to {file_path}")

        return HTMLResponse(file_content)


if __name__ == "__main__":
    uvicorn.run(app, host=configs['fastAPI']['HOST'], port=configs['fastAPI']['PORT'])
