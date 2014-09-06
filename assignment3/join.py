__author__ = 'acpigeon'

import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper(record):
    key = record[1]
    #print key
    #print record
    mr.emit_intermediate(key, record)


def reducer(key, list_of_values):

    tables_set = set([x[0] for x in list_of_values])
    tables = [t for t in tables_set]

    table_values = {}
    for t in tables:
        table_values[t] = []

    for t in tables:
        for l in list_of_values:
            if l[0] == t:
                table_values[t].append(l)

    for t1 in table_values[tables[0]]:
        for t2 in table_values[tables[1]]:
            mr.emit(t2 + t1)


if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
