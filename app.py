import os
from flask import Flask, Response, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
import asyncio
import requests
import json


application = Flask(__name__)
CORS(application)

async def nameEmailInformation(user_id):
    response = requests.get("http://registrationservice-env.eba-tg8ich7p.us-east-2.elasticbeanstalk.com/reg"
                            "-service/v1/users/" + str(user_id))
    user_info = response.json()
    name_email = user_info["first_name"] + ":" + user_info["username"]
    await asyncio.sleep(1)
    return name_email

async def get_collaborators(user_id, workspace_id):
    name_info = []
    response = requests.get("http://ec2-18-218-178-41.us-east-2.compute.amazonaws.com:5000/workspaces/" + str(user_id) + "/" + str(workspace_id) + "/collaborators")
    if response.status_code != 200:
        return None, (response.status_code, "Cannot get collaborators")
    response_json = response.json()
    for entry in response_json:
        user_id = entry['user']
        name_info.append(nameEmailInformation(user_id))
    information = []
    information.append(await asyncio.gather(*name_info))
    return information, None

@application.route('/workspaces/<user_id>/<workspace_id>/collaborators', methods=['GET'])
def collaboators_email(user_id, workspace_id):
    information, err = asyncio.run(get_collaborators(user_id, workspace_id))
    if err is not None:
        status, msg = err
        return Response(msg, status=status, content_type="text/plain")
    return Response(json.dumps(information, default=str), status=200, content_type="application/json")

@application.route('/', methods = ['GET'])
def respond_to_aws():
    return Response(status=200)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)