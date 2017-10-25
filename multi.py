from multiprocessing import Process
import time
def multi_factorial(N):
	halfN = N / 2
	p1 = Process(target=factorial1, args=[halfN,])
	p2 = Process(target=factorial2, args=[halfN, N,])

	p1.start()
	p2.start()

	p1.join()
	p2.join()
	
	print(p1 + p2)

def factorial1(N):
	result = 0
	while(N > 0):
		result += N
		N -= 1

	print(result)
	return result

def factorial2(M, N):
	result = 0

	while(M <= N):
		result += M
		M += 1

	print(result)
	return result



start = time.time()
N = 100000000

multi_factorial(N)

end = time.time()

print(end - start)