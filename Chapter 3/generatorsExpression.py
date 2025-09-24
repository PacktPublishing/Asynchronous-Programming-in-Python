from faker import Faker

fake = Faker()    
st = ((_,fake.name()) for _ in range(11))
curr_player = next(st)
print(f'Goalkeeper: {curr_player}')

for cp in st:
    print(f'Player: {cp}')
    
curr_player = next(st)
print(f'Goalkeeper {num}: {curr_player}')