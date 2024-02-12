from flask import Flask

# Creating an instance of Flask
app = Flask(__name__)

# Define a route to handle GET requests to the root URL '/'
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Starting the server on port 5000
if __name__ == '__main__':
    app.run(debug=True)
