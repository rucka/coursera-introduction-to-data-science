import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    id = record[0]
    code = record[1]
    mr.emit_intermediate(code[:-10], id)
    
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
