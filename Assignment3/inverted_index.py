import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    dwords = list(set(words))
    for w in dwords:
      mr.emit_intermediate(w, key)
	
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    data = []
    for v in list_of_values:
      data.append(v)
    mr.emit((key, data))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
