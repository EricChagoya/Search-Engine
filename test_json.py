import json
import random

"""
with open('0a0056fb9a53ec6f190aa2b5fb1a97c33cd69726c8841f89d24fa5abd84d276c.json', 'r') as f:
    array = json.load(f)

print (array)
print()

for k, v in array.items():
    print(k, v)
""" 
    

def unique_id(ids:{int}) -> int:
    """It returns random integer from 1000000 to 9999999 that
    is not already an id."""
    while True:
        num= random.randint(1000000, 9999999)
        if num not in ids:
            ids.add(num)
            return num
    
all_ids= set()
for i in range(5):
    a= unique_id(all_ids)
    print(a)

print(all_ids)


    
