import time

def pi_approximation(terms):
    numerator = 4.0
    denominator = 1.0
    sign = 1.0
    pi_approx = 0.0

    for _ in range(terms):
        pi_approx += sign * (numerator / denominator)
        sign *= -1
        denominator += 2

    return pi_approx

def pi_approximation_generator(terms):
    numerator = 4.0
    denominator = 1.0
    sign = 1.0
    pi_approx = 0.0

    for _ in range(terms):
        pi_approx += sign * (numerator / denominator)
        sign *= -1
        denominator += 2
        yield pi_approx

if __name__ == '__main__':
    num_iters = 1000000        
    for i in range(3):
        start = time.process_time_ns()
        pi_approx = pi_approximation(num_iters)
        end = time.process_time_ns()
        print(f'PI: {pi_approx} took {(end - start)/1000000000} seconds')
        start = time.process_time_ns()
        for approx in pi_approximation_generator(num_iters):
            pi_approx = approx
        end = time.process_time_ns()
        print(f'PIusing generator: {pi_approx} {(end - start)/1000000000} seconds')
