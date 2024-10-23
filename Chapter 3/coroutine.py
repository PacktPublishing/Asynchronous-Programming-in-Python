import numpy as np

def sim_temp(mean:float=15, stdv:float=5):
    rng = np.random.default_rng()
    temps = [rng.normal(mean, stdv) for _ in range(365)]
    yield min(temps), max(temps)
    threshold = (yield)
    print(f'Threshold: {threshold}')
    days_over_threshold = len([d for d in temps if d > threshold])
    print(f'There were:{days_over_threshold} days over {threshold} degrees')
    yield days_over_threshold
    
m = 22 
std = 8 
s = sim_temp(m, std) 
print(f'Simulating the temp around {m} with standard deviation of {std}') 
min, max = s.__next__()
print(f'The temp moves between {min} and {max} centigrades')
s.__next__()
s.send((max-min)/2)