# =========================== IMPORTS =========================== #
from flask import Blueprint, jsonify, request
import os, subprocess
import json

# =========================== CONFIG =========================== #
# create blueprint
gcp_blueprint = Blueprint("gcp_blueprint", __name__)

# Define routes
@gcp_blueprint.post("/gcp/prowler-scan")
def run_GCP_prowler_scan():
  # Retrieve the reuqest data
  data = request.get_json() or {}

  # Check if the project_id is part of the request body
  project_id = data.get('project_id')
  if not project_id:
      return jsonify({ "error": "Missing or empty 'project_id' in request body" }) 
  print(f"The selected project ID is {project_id}")

  # Create the path to the keyfile
  routes_dir = os.path.dirname(os.path.abspath(__file__))
  base_dir = os.path.dirname(routes_dir)
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

