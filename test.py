import random

for x in range(100):
    seed = str(random.randint(0,10))
    while(len(seed) != 5):
        seed = "0" + seed

    print(seed)
