import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[1]
    value = record

    mr.emit_intermediate(key, value)
	
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    order = None
    for v in list_of_values:
        if v[0] == 'order':
		    order = v
        else:
            mr.emit((order + v))
	
	
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
