from mpi4py import MPI
import gmpy2
import time
import math


def find_largest_gap(start, end):
    """Find the largest gap between consecutive prime numbers in the range [start, end]

    Args:
        start (int): start of the range
        end (int): end of the range

    Returns:
        int: largest gap
        int: first prime number
        int: second prime number
    """
    # Find the first prime number before start
    prev_prime = gmpy2.next_prime(start - 1)
    
    # Initialize the maximum gap
    max_gap = 0
    
    # Initialize the prime numbers
    prime1, prime2 = prev_prime, prev_prime

    # Iterate through the prime numbers in the range [start, end]
    while prev_prime < end:
        next_prime = gmpy2.next_prime(prev_prime)
        gap = next_prime - prev_prime
        
        # Update the maximum gap
        if gap > max_gap:
            max_gap = gap
            prime1, prime2 = prev_prime, next_prime
            
        # Update the previous prime number
        prev_prime = next_prime
        
    # Return the maximum gap and the prime numbers
    return max_gap, prime1, prime2

def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Initialize the range
    n = 1_000_000_000
    
    # Calculate the local range
    local_start = (rank - 1) * (n // (size - 1)) + 1
    local_end = (rank) * (n // (size - 1))

    if rank == size - 1:
        local_end = n

    
    start_time = time.time()
    local_max_gap, local_prime1, local_prime2 = find_largest_gap(local_start, local_end)
    
    # Gather the maximum gap and the prime numbers
    if rank == 0:
        global_max_gap = local_max_gap
        global_prime1 = local_prime1
        global_prime2 = local_prime2

        # Receive the maximum gap and the prime numbers from other processes
        for i in range(1, size):
            recv_max_gap, recv_prime1, recv_prime2 = comm.recv(source=i)
            if recv_max_gap > global_max_gap:
                global_max_gap = recv_max_gap
                global_prime1 = recv_prime1
                global_prime2 = recv_prime2

        # Print the results
        print(f"Largest gap: {global_max_gap} between primes {global_prime1} and {global_prime2}")
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
    else:
        # Send the maximum gap and the prime numbers to the root process
        comm.send((local_max_gap, local_prime1, local_prime2), dest=0)

if __name__ == "__main__":
    main()