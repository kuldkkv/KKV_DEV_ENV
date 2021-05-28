#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api

from factorial_c import Factorial

def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Factorial, '/factorial/<inp>')

    app.run(port = '5002')


if  __name__ == '__main__':
    main()




