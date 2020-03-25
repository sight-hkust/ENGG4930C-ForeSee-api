from chalice import Chalice
import random

app = Chalice(app_name='ForeSeeApi')


@app.route('/')
def index():
    i = random.randint(0, 1)
    if i == 1:
        return {'status': 'OK', 'message': 'My name is Charon, I carry information through the internet river.'}
    else:
        return {'status': 'OK',
                'message': 'Do you know the Trainman from Matrix? He is my uncle.'}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
