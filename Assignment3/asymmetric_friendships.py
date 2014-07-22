import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    person = record[0]
    friend = record[1]
    mr.emit_intermediate((person,friend),1)
    mr.emit_intermediate((friend, person),-1)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    sum = 0
    for v in list_of_values:
        sum = sum + v
    if sum != 0 : 
        mr.emit(key)
	'''
    values = []    
    for v in list_of_values:
        if v not in values:
            values.append(v)
    for v in values:
        mr.emit((key,v))
    '''

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
