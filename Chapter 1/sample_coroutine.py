import datetime 

def date_coroutine(_date:datetime.datetime): 
    print(f"Your appointment is scheduled for {_date.strftime('%m/%d/%Y, %H:%M:%S')}") 
    while True: 
        current_date = (yield) 
        if current_date > _date: 
            print("Ups, your appointment already passed") 
        else: 
            print("You have time") 

d1 = datetime.datetime(1981, 6, 29, 1, 0) 
coroutine = date_coroutine(d1) 
coroutine.__next__() 
d2 = datetime.datetime(2018, 5, 3) 
coroutine.send(d2)