import requests, time

def getData(URL="http://www.google.com", depth=5, funcToRun, funcArgs):
    try:
        funcToRun(*funcArgs)
    except:
        time.sleep(10)
        if depth > 0:
            print "Tried it again"
            getData("http://www.google.com", depth - 1)

if __name__ == '__main__':
    getData()
