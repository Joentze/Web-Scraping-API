from distutils.log import debug
from flask import Flask, request
from flask_restful import Resource, Api
from scrape import get_hrefs, get_texts, get_from_child_one, get_from_child_many
from rq import Queue
from worker import conn
import json
q = Queue(connection=conn)

app = Flask(__name__)
api = Api(app)


class scrape_hrefs(Resource):
    def get(self):
        get_received = request.get_json()
        link = get_received["link"]
        xpaths = get_received["xpaths"]
        return {'hrefs': get_hrefs(link, xpaths)}


class scrape_content(Resource):
    def get(self):
        get_received = request.get_json()
        link = get_received["link"]
        contents = get_received["article"]
        return {'article': get_texts(link, contents)}


class scrape_from_child_one(Resource):
    def get(self):
        get_received = request.get_json()
        results = q.enqueue(get_from_child_one, args=(str(get_received),))
        return {"results": results}


class scrape_from_child_many(Resource):
    def get(self):
        get_received = request.get_json()
        results = q.enqueue(get_from_child_many, args=get_received)
        return {"results": results}


class hello_world(Resource):
    def get(self):
        return "Hello World!"


api.add_resource(scrape_hrefs, '/scrape/href')
api.add_resource(scrape_content, '/scrape/article')
api.add_resource(scrape_from_child_one, '/scrape/from-child/one')
api.add_resource(scrape_from_child_many, '/scrape/from-child/many')
api.add_resource(hello_world, "/hello")
if __name__ == "__main__":
    app.run(debug=True)
