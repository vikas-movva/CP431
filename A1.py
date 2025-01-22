from mpi4py import MPI
import gmpy2
import time

def find_largest_gap(start, end):
    prev_prime = gmpy2.next_prime(start - 1)
    max_gap = 0
    prime1, prime2 = prev_prime, prev_prime

    while prev_prime < end:
        next_prime = gmpy2.next_prime(prev_prime)
        gap = next_prime - prev_prime
        if gap > max_gap:
            max_gap = gap
            prime1, prime2 = prev_prime, next_prime
        prev_prime = next_prime

    return max_gap, prime1, prime2

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    n = 1_000_000_000
    local_start = rank * (n // size) + 1
    local_end = (rank + 1) * (n // size)

    if rank == size - 1:
        local_end = n

    start_time = time.time()
    local_max_gap, local_prime1, local_prime2 = find_largest_gap(local_start, local_end)
    end_time = time.time()

    if rank == 0:
        global_max_gap = local_max_gap
        global_prime1 = local_prime1
        global_prime2 = local_prime2

        for i in range(1, size):
            recv_max_gap, recv_prime1, recv_prime2 = comm.recv(source=i)
            if recv_max_gap > global_max_gap:
                global_max_gap = recv_max_gap
                global_prime1 = recv_prime1
                global_prime2 = recv_prime2

        print(f"Largest gap: {global_max_gap} between primes {global_prime1} and {global_prime2}")
        print(f"Execution time: {end_time - start_time} seconds")
    else:
        comm.send((local_max_gap, local_prime1, local_prime2), dest=0)

if __name__ == "__main__":
    main()