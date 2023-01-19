import requests;
import json;
from flask import Flask,render_template,request,jsonify
from pymongo import MongoClient
from bs4 import BeautifulSoup

app = Flask(__name__)
with open('config.json', 'r') as f:
    config = json.load(f)        
    conn=MongoClient(config["MONGO"]["url"]);
    db=conn.PythonDB;
#영화정보 가져오기    
def findMovieInfo(params):
    movie_url = params["url"];
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    try:
        data = requests.get(movie_url,headers=headers)     
        # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
        # soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
        # 이제 코딩을 통해 필요한 부분을 추출하면 된다.
        # 영화 정보를 통해 가져옴 => naver가 아닐 경우에 대하여 에러처리를 해줘야한다.
        soup = BeautifulSoup(data.text, 'html.parser')
        #print(soup)  # HTML을 받아온 것을 확인할 수 있다.
        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')
        og_description = soup.select_one('meta[property="og:description"]')

        url_image = og_image['content']
        url_title = og_title['content']
        url_description = og_description['content']
        movieObj = {}
        if url_image is not None:
            movieObj = {"movie_url" : movie_url,"url_image" : url_image,"url_title":url_title,"url_description":url_description,"comment" : params["comment"]};
            db.movieInfo.insert_one(movieObj)
        return db.movieInfo.find_one({"url_title":url_title});
    except Exception as ex:
        print(ex);
        return {"url_image" : None};

    

@app.route('/')
def home():
   return render_template('index.html');

#데이터 호출
@app.route("/movies",methods=["get"])
def get_movieInfo():
    results=[]
    movies=list(db.movieInfo.find());   
    for movie in movies:
        movie['_id'] = str(movie['_id'])
        results.append(movie)
        
    return jsonify({"result":"success","movies":results});

#데이터 입력
@app.route("/movie",methods=["post"])
def input_movieInfo():
    #print(request.is_json)#json데이터가 존재하나?
    if request.is_json:
        params = request.get_json()#해당 데이터 바인딩
        #print(params)
        returnObj = findMovieInfo(params);
        if returnObj["url_image"] is not None:
            returnObj['_id'] = str(returnObj['_id']);
            return jsonify({"result":"success","resultCode":200,"article":returnObj});
        else :
            return jsonify({"result":"fail","resultCode":400});

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)



