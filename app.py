# =========================== IMPORTS =========================== #
from flask import Flask, jsonify, request
from flask_cors import CORS
import os, subprocess
from dotenv import load_dotenv
import json

# blueprints
from routes.gcp_blueprint import gcp_blueprint
from routes.aws_blueprint import aws_blueprint
# =========================== CONFIG =========================== #
# Create the app
app = Flask(__name__)
CORS(app)
load_dotenv()

# Register blueprints
app.register_blueprint(gcp_blueprint)
app.register_blueprint(aws_blueprint)

# Start the server
port = 8080
if __name__ == '__main__':
  app.run(debug=True, port=port)