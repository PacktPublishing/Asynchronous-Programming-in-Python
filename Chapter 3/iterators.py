from faker import Faker

class SoccerTeam():
    def __init__(self):
        fake = Faker()
        self.players = [fake.name() for _ in range(11)]
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.players):
            raise StopIteration
        else:
            player = self.players[self.current]
            self.current += 1
            return self.current, player
        
st = SoccerTeam()
st_iterator = iter(st)
num, curr_player = next(st_iterator)
print(f'Goalkeeper {num}: {curr_player}')

for n, cp in st:
    print(f'Player {n}: {cp}')
    
num, curr_player = next(st_iterator)
print(f'Goalkeeper {num}: {curr_player}')