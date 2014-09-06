import sys
import MapReduce

mr = MapReduce.MapReduce()


def mapper(record):
    seen_words = []
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
        if w not in seen_words:
            seen_words.append(w)
            mr.emit_intermediate(w, key)


def reducer(key, list_of_values):
    mr.emit((key, list_of_values))


if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)