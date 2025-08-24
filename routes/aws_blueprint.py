# =========================== IMPORTS =========================== #
from flask import Blueprint, jsonify, request
import os, subprocess
import json

# =========================== CONFIG =========================== #
# create blueprint
aws_blueprint = Blueprint("aws_blueprint", __name__)

@aws_blueprint.post("/aws/prowler-scan")
def run_AWS_prowler_scan():
  # Retrieve the reuqest data
  data = request.get_json() or {}

  # Check if the resource_arn is part of the request body
  resource_arn = data.get('resource_arn') # ARN = Amazon Resource Name
  if not resource_arn:
      return jsonify({ "error": "Missing or empty 'resource_arn' in request body" }) 
  print(f"The selected resource ARN is {resource_arn}")

  # Define the command
  command = [
    "prowler",
    "aws",
    "--resource-arn", resource_arn,
    "-M", "json",
    "--output-filename", "aws-security-audit",
    "--output-directory", "aws-output"
  ]

  # Execute the command
  subprocess.run(
    command,
    capture_output=True,
    text=True, # Decode stdout/stderr as text
    check=False # Don't raise an exception for non-zero exit codes
  )

  # Create the path to the keyfile
  routes_dir = os.path.dirname(os.path.abspath(__file__))
  base_dir = os.path.dirname(routes_dir)

  # Create the path to the output file
  aws_output_filepath = os.path.join(base_dir, "aws-output", "aws-security-audit.json")

  # Send the results back in JSON format
  try:
    # Open the output file 
    with open(aws_output_filepath, "r") as aws_scan_output:
      # Transform the file handle into a Python dictionary
      data = json.load(aws_scan_output)

      return jsonify(data)
  except FileNotFoundError:
      return jsonify({"error": "File not found"}), 404
  finally:
      #  Check if the file exists before deleting it
      if os.path.exists(aws_output_filepath):
         os.remove(aws_output_filepath)
         print("Successfully deleted AWS scan output file")
  