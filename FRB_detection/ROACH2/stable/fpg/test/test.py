import numpy as np

with open('test', 'w') as f:
    count =0
    while(1):
        f.seek(0)
        f.truncate()
        if(count == 1023):
            count = 0
        else:
            count = count+1
        f.write(str(count))

