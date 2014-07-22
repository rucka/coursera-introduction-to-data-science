import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    matrix = record[0]
    i = record[1]
    j = record[2]
    v = record[3]
    
    for k in range(0,5):
        if (matrix == 'a'):
            mr.emit_intermediate((i, k), record)
        else:    		
            mr.emit_intermediate((k, j), record)
    
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
 
    valA = [0,0,0,0,0]
    valB = [0,0,0,0,0]
    for v in list_of_values:
        if v[0] == 'a':                          
            valA[v[2]] = v[3]                  
        else:                      
            valB[v[1]] = v[3]                  
    sum = 0                          
    for i in range(0,5):                          
        sum = sum + valA[i]*valB[i]                      
    mr.emit((key[0], key[1], sum))        
		
		
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
