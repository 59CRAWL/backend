
import datetime
import pandas as pd

"""
Define Queue for berths
"""
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        
    def get_last(self):
        if not self.is_empty():
            return self.items[-1]

    def size(self):
        return len(self.items)

""""
Begins algorithm to adjust time sheet and push ships around until expected times
"""
# Create queues
#   1 for each berth that is being used
#       Data that should be populated with should look like [EDT, EDT, EDT, ...]
n = 2
berths = [Queue() for _ in range(n)]

# 1. Call Machine Learning model with a input CSV file
data = [{"shipId": 1, "EAT": datetime.datetime.now(),"EDT": datetime.datetime.now() + datetime.timedelta(days=7)}, 
        {"shipId": 2, "EAT": datetime.datetime.now() - datetime.timedelta(days=7), "EDT": datetime.datetime.now() + datetime.timedelta(days=1)},
        {"shipId": 1, "EAT": datetime.datetime.now(),"EDT": datetime.datetime.now() + datetime.timedelta(days=7)}, 
        {"shipId": 2, "EAT": datetime.datetime.now() - datetime.timedelta(days=7), "EDT": datetime.datetime.now() + datetime.timedelta(days=1)}]

df = pd.DataFrame.from_dict(data)

# 2. Sort the ships by Expected Arrival Time
df.sort_values(by="EAT", inplace=True)

# Insert expected added values later
df["Berth"] = 0
df["On Time"] = None

# 3. Loop through ship arrival times
for idx, ship in df.iterrows():
    arrival = ship.get("EAT")
    departure = ship.get("EDT")
    on_time = False

    # 4. Loop through the berths to find empty berths
    for i in range(len(berths)):
        berth = berths[i]

        # 4.1. Kick out ships once EDTs have passed
        for edt in berth.items:
            if edt < arrival:
                berth.dequeue()
            else:
                break

        # 4.2. Allocate a ship to empty berth
        if berth.is_empty():
            # Update berth with EDT and update ship details
            berth.enqueue(departure)
            df.at[idx, "Berth"] = i
            df.at[idx, "On Time"] = True
            on_time = True
            break
    
    # 5. If berths are full, indicate new docking time if necessary
    if not on_time:
        # 5.1. Find the earliest EDT for the docks
        earliest_departure = datetime.datetime.max
        next_berth = -1
        for index, berth in enumerate(berths):
            edt = berth.get_last()
            if edt < earliest_departure:
                earliest_departure = edt
                next_berth = index
        
        df.at[idx, "Berth"] = next_berth
        df.at[idx, "On Time"] = False

        # 5.2. Calculate the updated estimated departure time and adjust in the sheets
        departure += earliest_departure - arrival
        berths[next_berth].enqueue(departure)
        df.at[idx, "EDT"] = departure
        df.at[idx, "EAT"] = earliest_departure

print(df)