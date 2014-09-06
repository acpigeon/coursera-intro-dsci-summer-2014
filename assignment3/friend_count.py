__author__ = 'acpigeon'

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    mr.emit_intermediate(record[0], record[1])

def reducer(key, list_of_values):
    friend_set = set(list_of_values)
    mr.emit((key, len(friend_set)))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
