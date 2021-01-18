import requests
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/articulos', methods=['POST'])
def create_article():
    #Receiving data
    title = request.json['title']
    url = request.json['url']

    if title and url:
        #Save to mongo
        mongo.db.articles.insert(
            {
                'title': title,
                'url': url
            }
        )
        data = {'message':'received'}
    else:
        data = {'message':'error'}

    return jsonify(data)


@app.route('/getnews')
def getArticles():
    resp = requests.get(
        url="https://api.nytimes.com/svc/topstories/v2/business.json?api-key=XW7AM6JluoNs9k9U7bzChxA29XDeWW5g")
    if resp.status_code != 200:
        # This means something went wrong
        print("error de api")
        raise requests.HTTPError(resp.status_code)
    json_object = resp.json()
    for article_item in json_object['results']:
        title = article_item['title']
        abstract = article_item['abstract']
        url = article_item['url']
        byline = article_item['byline']
        multimedia = article_item['multimedia']

        mongo.db.articles.insert(
            {
                'title': title,
                'abstract': abstract,
                'url': url,
                'author': byline,
                'multimedia':multimedia
            }
        )


    data = {'message': 'received'}
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True)


