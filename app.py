import requests;
import json;
from flask import Flask,render_template,request,jsonify
from pymongo import MongoClient
app = Flask(__name__)
with open('config.json', 'r') as f:
    config = json.load(f)        
    conn=MongoClient(config["MONGO"]["url"]);
    db=conn.PythonDB;
#영화정보 가져오기    
def findMovieInfo(movie_url):
    print(movie_url);   

@app.route('/')
def home():
   return render_template('index.html');

#데이터 호출
@app.route("/movie",methods=["get"])
def get_movieInfo():
    movie=db.movieInfo.find_one({"title":"매트릭스"});   
   
    return jsonify({"title":movie["title"],"point":movie["point"]});

#데이터 입력
@app.route("/movie",methods=["post"])
def input_movieInfo():
    #print(request.is_json)#json데이터가 존재하나?
    if request.is_json:
        params = request.get_json()#해당 데이터 바인딩
        #print(params)
        findMovieInfo(params["url"]);
    return jsonify({"result":"success","resultCode":200});
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)



