__author__ = 'acpigeon'

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    mr.emit_intermediate((record[0], record[1]), 1)
    mr.emit_intermediate((record[1], record[0]), 1)

def reducer(key, list_of_values):
    total = 0
    for v in list_of_values:
      total += v

    output = []
    if total == 1:
        if key not in output:
            output.append(tuple(key))

    for o in set(output):
        mr.emit(o)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
