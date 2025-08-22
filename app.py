# =========================== IMPORTS =========================== #
from flask import Flask
from flask_cors import CORS

# =========================== CONFIG =========================== #
# Create the app
app = Flask(__name__)
CORS(app)

# Define home route
@app.route("/")
def hello_world():
  return "Hello, world"

# Start the server
port = 8080
if __name__ == '__main__':
  app.run(debug=True, port=port)