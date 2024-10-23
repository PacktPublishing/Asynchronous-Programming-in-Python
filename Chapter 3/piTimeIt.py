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
    import timeit
    print(timeit.timeit("pi_approximation(1000000)", setup="from __main__ import pi_approximation", number=100))
    print(timeit.timeit("pi_approximation_generator(1000000)", setup="from __main__ import pi_approximation_generator", number=100))