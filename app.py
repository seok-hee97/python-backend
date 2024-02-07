from flask import Flask,request ,jsonify        #플라스크 클래스 임포트
# through request http request read json data
#jsonify dict object-> json & HTTP response

from flask.json import JSONEncoder

##Dafualt JSON encoder can't convert set()-> json
## so make CustomEncoder func: set->list
##list can convert json
class CustomJSONEnocder(JSONEncoder):
    def default(self, obj):
        if isinstance(self, set):
            return list(obj)
        
        return JSONEncoder.default(self, obj)


app = Flask(__name__)           #Flask 클래스를 객체화(instantiate)시켜서 app 이라는 변수에 저장
app.users = {} 
# new user save at user dict
# key: id  / value : user info

app.id_count = 1
# save id var
# when save user  +1
app.tweet = []
app.json_encoder = CustomJSONEnocder


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

                                        
@app.route("/sign-up", methods = ['POST'])
def sign_up():
    new_user                =request.json
    # request는 엔드포인트에 전송된 HTTP요청 정보를 저장(*JSON)
    # .json은 위에 json  convert to python dict로 변환
    # result : new_user -> python dict data
    new_user["id"]          =app.id_count
    # new_user dict dict(name)['key value']= value
    # new_user id key   app.id_count라는 value match
    app.users[app.id_count] =new_user
    # app.user도 위에서 dict로 열어놨음
    # app.id_count에 해당하는 키값에 new_user라는 value를 매치
    app.id_count            =app.id_count +1                                        

    return jsonify(new_user)
    #new_user를 python dict 자료형으로 변환하여 return


@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']
    
    if user_id not in app.users:
        return 'Not qualified User', 400
    
    if len(tweet) > 300:
        return 'Do not over 300', 400
    user_id = int(payload['id'])
    
    app.tweet.append({
        'user.id' : user_id,
        'tweet' : tweet
        })
    return '', 200


@app.route('/follow', methods=['POST'])
def follow():
    payload	      = request.json
    user_id	      = int(payload['id'])
    user_id_to_follow = int(payload['follow'])
    
    if user_id not in app.users or user_id_to_follow not in app.users:
        return 'undefined user', 400
    
    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)
    
    return jsonify(user)




@app.route('/unfollow', methods = ['POST'])
def unfollow():
    payload =   request.json
    user_id =   int(payload['id'])
    user_id_to_follow   = int(payload['unfollow'])
    
    
    if user_id not in app.users or user_id_to_follow not in app.users:
        return ' no user exist', 400
    
    user= app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)
    
    
    return jsonify(user)



@app.route('/timeline/<int:user_id>', methods = ['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return ' no user exists', 400
    
    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]
    
    
    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })