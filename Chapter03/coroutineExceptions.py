import numpy as np

def sim_temp(mean:float=15, stdv:float=5):
    try:
        rng = np.random.default_rng()
        temps = [rng.normal(mean, stdv) for _ in range(365)]
        yield min(temps), max(temps)
        threshold = (yield)
        print(f'Threshold: {threshold}')
        days_over_threshold = len([d for d in temps if d > threshold])
        print(f'There were:{days_over_threshold} days over {threshold} degrees')
        yield days_over_threshold
    except GeneratorExit:
        print('This is already closed')
        return 0
try:
    m = 22 
    std = 8 
    s = sim_temp(m, std) 
    print(f'Simulating the temp around {m} with standard deviation of {std}') 
    min, max = s.__next__()
    s.close()
    print(f'The temp moves between {min} and {max} centigrades')
    s.__next__()
    s.send((max-min)/2)
except StopIteration:
    print('Nothing else in the coroutine')