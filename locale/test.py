from sqids import Sqids
sqids = Sqids()

from time import time
from random import randint

seed = int(time())
random_component = randint(0, 100000)
print(seed, random_component)
id = sqids.encode([seed, random_component]) # "86Rf07"
numbers = sqids.decode(id) # [1, 2, 3]

print(id)