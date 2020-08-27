#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
#from flask.ext.jsonpify import jsonify
import psycopg2
from waitress import serve


class Employees(Resource):
    def __init__(self):
        self.conn = psycopg2.connect(host="openbsd.64",database="pgdb1", user="kkv1", password="point007")
        
    def get(self):
        #return {'employees' : [1, 2, 3, 4, 5]}
        self.cur = self.conn.cursor()
        self.cur.execute('select * from employee');
        return {'employees' : [str(i[0]) + ':' + i[1] + ':' + i[2] for i in self.cur.fetchall()]}
        self.cur.close()


class Dept(Resource):
    def __init__(self):
        self.conn = psycopg2.connect(host="openbsd.64",database="pgdb1", user="kkv1", password="point007")

    def get(self):
        self.cur = self.conn.cursor()
        self.cur.execute('select * from dept')
        return {'dept' : [str(i[0]) + ':' + i[1] for i in self.cur.fetchall()]}
        self.cur.close()
        #return {'dept' : ['D1', 'D2', 'D3', 'D4 a', 'D4 b', 'D5', 'D6']}

class Employee(Resource):
    def get(self, employee_id):
        emp_id = int(employee_id)

        if emp_id == 1:
            return {'employee' : {'id' : 1, 'name' : 'employee 1'}}
        elif emp_id == 2:
            return {'employee' : {'id' : 2, 'name' : 'employee 2'}}
        elif emp_id == 3:
            return {'employee' : {'id' : 3, 'name' : 'employee 3'}}
        elif emp_id == 4:
            return {'employee' : {'id' : 4, 'name' : 'employee 4'}}
        elif emp_id == 5:
            return {'employee' : {'id' : 5, 'name' : 'employee 5'}}
        else:
            return None



def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Employees, '/employees')
    api.add_resource(Dept, '/dept')
    api.add_resource(Employee, '/employee/<employee_id>')

    #app.run(host = '0.0.0.0', port = '5002')
    serve(app, host = '0.0.0.0', port = '5002')



if __name__ == '__main__':
    main()
