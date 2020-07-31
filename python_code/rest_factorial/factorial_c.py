#!/usr/bin/env python

from flask_restful import Resource
import os


class Factorial(Resource):

    def get(self, inp):

        stream = os.popen("./fact " + inp)
        output = stream.read().rstrip()

        return output
                    
