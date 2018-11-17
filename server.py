from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/animate', methods=['POST'])
def animate():
    print(request.get_json()[0]['to'])
    return 'kek'
