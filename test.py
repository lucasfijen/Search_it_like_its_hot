from multiprocessing import Pool
import os

class Engine(object):
    def __call__(self, n):
        f = factorial(n)
        print(f)
        return 

def factorial(n):
    result = 0

    while (n > 0):
        result += n
        n -= 1

    return result


try:
    pool = Pool(os.cpu_count()) # on 8 processors
    engine = Engine()
    n = 100000000
    data_input = [n,n,n,n,n,n,n,n,n,n,n,n]
    data_outputs = pool.map(engine, data_input)
finally: # To make sure processes are closed in the end, even if errors happen
    pool.close()
    pool.join()