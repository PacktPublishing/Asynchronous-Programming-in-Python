from faker import Faker

def soccer_team():
    fake = Faker()
    for current in range(11):
        yield current, fake.name()
        current += 1
        
st = soccer_team()
num, curr_player = next(st)
print(f'Goalkeeper {num}: {curr_player}')

for n, cp in st:
    print(f'Player {n}: {cp}')
    
num, curr_player = next(st)
print(f'Goalkeeper {num}: {curr_player}')