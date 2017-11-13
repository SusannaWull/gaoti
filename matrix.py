import time

#calculate run time
def run_time(func):
	def wrapper(*args,**kwargs):
		t1 = time.time()
        	func(*args,**kwargs)
        	t2 = time.time()
        	print "%s run time: %.5f s" %(func.__name__,t2-t1)
	return wrapper
	

#function for generating matrix,whose size is  N*N, elements are all k
def gen_matrix(N,k):
	return [[k for i in range(N)] for i in range(N)]
		
		

@run_time
def soluiton_mo(A,B,C,n):
	"""
	Solution M0,naive loop. Parameters are as follow:
	A,B,C:
		N*N matrix
	n:
		loop times
	"""
	N = len(A[0])
	for _ in range(n):
		#C=A*B
		for i in range(N):
			for j in range(N):
				for k in range(N):
					C[i][j] += A[i][k]*B[k][j]

		#B=C*A
		for i in range(N):
			for j in range(N):
				for k in range(N):
					B[i][j] += C[i][k]*A[k][j]
		#A=B*C
		for i in range(N):
			for j in range(N):
				for k in range(N):
					A[i][j] += B[i][k]*C[k][j]
	

@run_time
def solution_m1(A,B,C,n):
	"""
	Solution M1,transpose matrix first. Parameters are as follow:
	A,B,C:
		N*N matrix
	n:
		loop times
	"""
	N = len(A[0])
	for _ in range(n):
		#C=A*B
		temp = B
		for i in range(N):
			for j in range(N):
				temp[i][j] = B[j][i]  #transpose B first
		
		for i in range(N):
			for j in range(N):
				for k in range(N):
					C[i][j] += A[i][k]*temp[j][k]

		#B=C*A
		temp = A
		for i in range(N):
			for j in range(N):
				temp[i][j] = A[j][i]  #transpose A first
		
		for i in range(N):
			for j in range(N):
				for k in range(N):
					B[i][j] += C[i][k]*temp[j][k]

		#A=B*C
		temp = C
		for i in range(N):
			for j in range(N):
				temp[i][j] = C[j][i]  #transpose C first

		for i in range(N):
			for j in range(N):
				for k in range(N):
					A[i][j] += B[i][k]*temp[j][k]



def solution_m234(A,B,C,block_size,n):
	"""
	Solution M2,multiply by blocking. Parameters are as follow:
	A,B,C:
		N*N matrix

	block_size:
		the size of block
	n:
		loop times

	"""
	N = len(A[0])
	for _ in range(n):
		#C=A*B
		temp = B
		for i in range(N):
			for j in range(N):
				temp[i][j] = B[j][i]  #transpose B first
		
		for jj in range(0,N,block_size):
			for kk in range(0,N,block_size):
				temp_j = min(jj+block_size,N)
				temp_k = min(kk+block_size,N)
			for i in range(N):
				for j in range(jj,temp_j):
					r = 0
					for k in range(kk,temp_k):
						r += A[i][k]*temp[j][k]
					C[i][j] += r
		
		#B=C*A
		temp = A
		for i in range(N):
			for j in range(N):
				temp[i][j] = A[j][i]  #transpose A first
		
		for jj in range(0,N,block_size):
			for kk in range(0,N,block_size):
				temp_j = min(jj+block_size,N)
				temp_k = min(kk+block_size,N)
			for i in range(N):
				for j in range(jj,temp_j):
					r = 0
					for k in range(kk,temp_k):
						r += C[i][k]*temp[j][k]
					B[i][j] += r

		#A=B*C
		temp = C
		for i in range(N):
			for j in range(N):
				temp[i][j] = C[j][i]  #transpose C first
		
		for jj in range(0,N,block_size):
			for kk in range(0,N,block_size):
				temp_j = min(jj+block_size,N)
				temp_k = min(kk+block_size,N)
			for i in range(N):
				for j in range(jj,temp_j):
					r = 0
					for k in range(kk,temp_k):
						r += B[i][k]*temp[j][k]
					A[i][j] += r
		
	

@run_time
def solution_m2(A,B,C,n):
	block_size = 4
	solution_m234(A,B,C,block_size,n)

@run_time
def solution_m3(A,B,C,n):
	block_size = 8
	solution_m234(A,B,C,block_size,n)

@run_time
def solution_m4(A,B,C,n):
	block_size = 16
	solution_m234(A,B,C,block_size,n)

@run_time
def solution_m5(A,B,C,n):
	block_size = 32
	solution_m234(A,B,C,block_size,n)

@run_time
def solution_m6(A,B,C,n):
	block_size = 64
	solution_m234(A,B,C,block_size,n)
	
	

if __name__ == "__main__":
	N_list = (128,256,512,1024,2048)
	n_list = (4096,512,64,8,1)
	for i in range(len(N_list)):
		N = N_list[i]
		n = n_list[i]
		print "Matrix size {0}*{0},loop times:{1}".format(N,n)
		A,B,C = gen_matrix(N,0),gen_matrix(N,0),gen_matrix(N,0)  #set matrix element to 0, we had tried 1,2... and it become too slow. 
		soluiton_mo(A,B,C,n)
		solution_m1(A,B,C,n)
		solution_m2(A,B,C,n)
		solution_m3(A,B,C,n)
		solution_m4(A,B,C,n)
		solution_m5(A,B,C,n)
		solution_m6(A,B,C,n)
