from flask import Flask, jsonify, request, Response
import json
import jwt
import urllib.request, json
import sys

public_keys = {}
app = Flask(__name__)

SERVICE_ID = "api://sampleserviceA"

@app.route('/data')
def data():
    try:
        validate_JWT(request.headers['Authorization'])
        return jsonify({ "data": 1 })
    except Exception as e:
        print(e)
        return Response("Forbidden", status=403)

def init():
    jwks = {}
    # Fetch jwks from Azure AD URL
    with urllib.request.urlopen("https://login.microsoftonline.com/ebf8eafe-72d9-4d75-9eef-0816103eeb79/discovery/v2.0/keys") as url:
        jwks = json.loads(url.read().decode())

    # Get Keys from JWKS
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

def validate_JWT(header):
    token = header[7:]
    
    # Get kid from Header
    kid = jwt.get_unverified_header(token)['kid']
    key = public_keys[kid]

    # Decode using Public Key
    jwt.decode(token, key=key, audience=SERVICE_ID, algorithms=['RS256'])
        

init()