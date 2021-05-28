import os

def get(inp):
	stream = os.popen("/home/kkv/KKV_DEV_ENV/python_code/rest_factorial/fact " + inp)
	output = stream.read()
	return output

x = get("4")
print (x)
