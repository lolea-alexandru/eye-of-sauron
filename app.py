# =========================== IMPORTS =========================== #
from flask import Flask, jsonify, request
from flask_cors import CORS
import os, subprocess, shlex
from dotenv import load_dotenv
import json
# =========================== CONFIG =========================== #
# Create the app
app = Flask(__name__)
CORS(app)
load_dotenv()

# Define home route
@app.post("/gcp/prowler-scan")
def run_GCP_prowler_scan():
  # Retrieve the reuqest data
  data = request.get_json() or {}

  # Check if the porject_id is part of the request body
  project_id = data.get('project_id')
  if not project_id:
      return jsonify({ "error": "Missing or empty 'project_id' in request body" }) 
  print(f"The selected project ID is {project_id}")

  # Create the path to the keyfile
  base_dir = os.path.dirname(os.path.abspath(__file__))
  key_filepath = os.path.join(base_dir, "SA_key.json")

  # Define command
  command = [
    "prowler", 
    "gcp",                              
    "--credentials-file", key_filepath,
    "--project-id", project_id,
    "-M", "json",
    "--output-filename", "gcp-security-audit",
    "--output-directory", "gcp-output"
  ]

  # Execute the command
  subprocess.run(
    command,
    capture_output=True,
    text=True, # Decode stdout/stderr as text
    check=False # Don't raise an exception for non-zero exit codes
  )


  # Create the path to the output file
  gcp_output_filepath = os.path.join(base_dir, "gcp-output", "gcp-security-audit.json")

  # Send the results back in JSON format
  try:
    # Open the output file 
    with open(gcp_output_filepath, "r") as gcp_scan_output:
      # Transform the file handle into a Python dictionary
      data = json.load(gcp_scan_output)

      return jsonify(data)
  except FileNotFoundError:
      return jsonify({"error": "File not found"}), 404
  finally:
      #  Check if the file exists before deleting it
      if os.path.exists(gcp_output_filepath):
         os.remove(gcp_output_filepath)
         print("Successfully deleted GCP scan output file")


# Start the server
port = 8080
if __name__ == '__main__':
  app.run(debug=True, port=port)