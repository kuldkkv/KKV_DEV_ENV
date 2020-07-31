#!/usr/bin/env python

from flask_restful import Resource


class Factorial(Resource):

    def get(self, inp):
        inp_l = int(inp)

        if inp_l <= 1:
            return 1
        return inp_l * self.get(inp_l-1)
                    
