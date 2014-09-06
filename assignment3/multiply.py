__author__ = 'acpigeon'

import MapReduce
import sys

mr = MapReduce.MapReduce()


# A is m x n matrix, B is n x k.
# For this problem, we are given that m == n == k == 5.


def mapper(record):
    """
    record = [matrix, row, col, val]
    For matrix A, emit k values for each row. For matrix B, emit k values for each column. Specifically:
    For each A(i,j) emit (i, k), [matrix, j, value] for k = 0:4
    For each B(i,j) emit (k, j), [matrix, i, value] for k = 0:4
    """

    mat = record[0]
    row = record[1]
    col = record[2]
    val = record[3]

    for k in xrange(5):
        if mat == 'a':
            #print "Matrix a: " + str((row, k)) + ", " + str((mat, col, val))
            mr.emit_intermediate((row, k), (mat, col, val))
        else:
            #print "Matrix b: " + str((k, col)) + ", " + str((mat, row, val))
            mr.emit_intermediate((k, col), (mat, row, val))


def reducer(key, list_of_values):
    """
    Reducer input has the output matrix position (i,j) and the lists of values, e.g.:
    (3, 2)
        [(u'a', 0, 24), (u'a', 1, 79), (u'a', 2, 24), (u'a', 3, 47), (u'a', 4, 18),
         (u'b', 0, 89), (u'b', 1, 34), (u'b', 2, 49), (u'b', 3, 85), (u'b', 4, 33)]
    Not all matrix positions are returned, and a value of 0 is assume for this case.

    Reducer should calculate the value the value of this cell, e.g.:
    (3, 2) = (24 * 89) + (79 * 34) + (24 * 49) + (47 * 85) + (18 * 33) = 2136 + 2686 + 1176 + 3995 + 594 = 10587

    Reducer should return the output matrix position and the proper value: ((i, j), x)
    """

    # Hacky fix for missing values
    val_dict = {0: {'a': 0, 'b': 0}, 1: {'a': 0, 'b': 0}, 2: {'a': 0, 'b': 0}, 3: {'a': 0, 'b': 0}, 4: {'a': 0, 'b': 0}}
    for val in list_of_values:
        val_dict[val[1]][val[0]] = val[2]

    output = 0
    for position in val_dict.keys():
        output += val_dict[position]['a'] * val_dict[position]['b']

    mr.emit((key[0], key[1], output))


if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
