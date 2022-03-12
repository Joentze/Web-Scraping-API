from distutils.log import debug
from flask import Flask, request
from flask_restful import Resource, Api
from scrape import get_hrefs, get_texts

app = Flask(__name__)
api = Api(app)

class scrape_hrefs(Resource):
    def get(self):
        post_received = request.get_json()
        link = post_received["link"]
        xpaths = post_received["xpaths"]
        return {'hrefs':get_hrefs(link, xpaths)}

class scrape_content(Resource):
    def get(self):
        post_received = request.get_json()
        link = post_received["link"]
        contents = post_received["article"]
        return {'article':get_texts(link, contents)}

api.add_resource(scrape_hrefs, '/scrape/href')
api.add_resource(scrape_content, '/scrape/article')

if __name__ == "__main__":
    app.run(debug=True)