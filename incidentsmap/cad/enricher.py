import json

class Enricher(object):
    def __init__(self, fname):
        print('Enricher construct.')
        with open(fname, 'r') as json_file:
            data = json.load(json_file)
            print(data)

