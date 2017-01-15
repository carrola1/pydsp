import numpy as np

patterni  = "{0:08b}".format(int(0x53))
pattern = np.array(list(map(int,patterni)),dtype=int)
print(pattern)
