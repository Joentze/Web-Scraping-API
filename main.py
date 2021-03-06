from distutils.log import debug
from flask import Flask, request
from flask_restful import Resource, Api
from scrape import get_hrefs, get_texts, get_from_child_one, get_from_child_many

app = Flask(__name__)
api = Api(app)

class scrape_hrefs(Resource):
    def get(self):
        get_received = request.get_json()
        link = get_received["link"]
        xpaths = get_received["xpaths"]
        return {'hrefs':get_hrefs(link, xpaths)}

class scrape_content(Resource):
    def get(self):
        get_received = request.get_json()
        link = get_received["link"]
        contents = get_received["article"]
        return {'article':get_texts(link, contents)}

class scrape_from_child_one(Resource):
    def get(self):
        get_received = request.get_json()
        return {"results":get_from_child_one(get_received)}

class scrape_from_child_many(Resource):
    def get(self):
        get_received = request.get_json()
        return {"results":get_from_child_many(get_received)}

class hello_world(Resource):
    def get(self):
        return "Hello World!"


api.add_resource(scrape_hrefs, '/scrape/href')
api.add_resource(scrape_content, '/scrape/article')
api.add_resource(scrape_from_child_one,'/scrape/from-child/one')
api.add_resource(scrape_from_child_many,'/scrape/from-child/many')
api.add_resource(hello_world, "/hello")
if __name__ == "__main__":
    app.run(debug=True)