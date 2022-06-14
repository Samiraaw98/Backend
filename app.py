from flask import Flask, jsonify, request
from flask_cors import CORS
from db_helpers import run_query
import sys

app = Flask(__name__)
CORS(app)


@app.get('/api/post')
def blog_get():
    post_list = run_query("SELECT * from posts")
    resp = []
    for post in post_list:
        an_obj={}
        an_obj['userId'] = post[0]
        an_obj['username'] = post[1]
        an_obj['userPost'] = post[2]
        resp.append(an_obj)
    return jsonify(resp) , 200
    
@app.post('/api/post')
def blog_post():
    data = request.json
    username = data.get('username')
    user_post = data.get('userPost')
    if not username:
        return jsonify("Missing required argument :username")
    if not user_post :
        return jsonify("Missing required argyment :userPost")
    run_query("INSERT INTO posts(username, posts) VALUES(?,?)" , [username, user_post])
    return jsonify("post added"), 201

if len(sys.argv) >1:
    mode = sys.argv[1]
else :
    print("Missing required mode argument")

if mode == 'testing':
    CORS(app)
    print("Runnng in testing mode !")
    app.run(debug=True)
elif mode == "production" :
        import bjoern
        print("Running in production mode!")
        bjoern.run(app, "0.0.0.0" , 5005)
else:
    print("Invalid mode , must be one of :testing | production")
    exit()