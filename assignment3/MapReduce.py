import json

class MapReduce:
    def __init__(self):
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)
        #print "self.intermediate:"
        #print json.dumps(self.intermediate, sort_keys=True, indent=4, separators=(',', ': '))
        #print ""

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        for line in data:
            record = json.loads(line)
            mapper(record)

        for key in self.intermediate:
            reducer(key, self.intermediate[key])
            #print "self.intermediate[key]:"
            #print key
            #print json.dumps(self.intermediate[key], sort_keys=True, indent=4, separators=(',', ': '))
            #print ""

        #jenc = json.JSONEncoder(encoding='latin-1')
        jenc = json.JSONEncoder()
        for item in self.result:
            print jenc.encode(item)
