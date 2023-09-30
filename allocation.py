
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
berth_count = 10

def allocation(csvfile):
    # 1. Read csvfile as a pandas dataframe
    # df = pd.read_csv(csvfile)
    
    """
    Testing data for user
    """
    data = [{"shipId": 1, "ETA": datetime.datetime.now(),"ETD": datetime.datetime.now() + datetime.timedelta(days=7)}, 
            {"shipId": 2, "ETA": datetime.datetime.now() - datetime.timedelta(days=7), "ETD": datetime.datetime.now() + datetime.timedelta(days=1)},
            {"shipId": 1, "ETA": datetime.datetime.now(),"ETD": datetime.datetime.now() + datetime.timedelta(days=7)}, 
            {"shipId": 2, "ETA": datetime.datetime.now() - datetime.timedelta(days=7), "ETD": datetime.datetime.now() + datetime.timedelta(days=1)}]

    df = pd.DataFrame.from_dict(data)

    # 2. Sort the ships by Expected Arrival Time
    df.sort_values(by="ETA", inplace=True)

    # Insert expected added values later
    df["Berth"] = 0
    df["On Time"] = None

    # Creating queues, 1 for each berth that exists
    #   Data that should be populated with should look like [ETD, ETD, ETD, ...]
    berths = [Queue() for _ in range(berth_count)]

    # 3. Loop through ship arrival times
    for idx, ship in df.iterrows():
        arrival = ship.get("ETA")
        departure = ship.get("ETD")
        on_time = False

        # 4. Loop through the berths to find empty berths
        for i in range(len(berths)):
            berth = berths[i]

            # 4.1. Kick out ships once ETDs have passed
            for ETD in berth.items:
                if ETD < arrival:
                    berth.dequeue()
                else:
                    break

            # 4.2. Allocate a ship to empty berth
            if berth.is_empty():
                # Update berth with ETD and update ship details
                berth.enqueue(departure)
                df.at[idx, "Berth"] = i
                df.at[idx, "On Time"] = True
                on_time = True
                break
        
        # 5. If berths are full, indicate new docking time if necessary
        if not on_time:
            # 5.1. Find the earliest ETD for the docks
            earliest_departure = datetime.datetime.max
            next_berth = -1
            for index, berth in enumerate(berths):
                ETD = berth.get_last()
                if ETD < earliest_departure:
                    earliest_departure = ETD
                    next_berth = index
            
            df.at[idx, "Berth"] = next_berth
            df.at[idx, "On Time"] = False

            # 5.2. Calculate the updated estimated departure time and adjust in the sheets
            departure += earliest_departure - arrival
            berths[next_berth].enqueue(departure)
            df.at[idx, "ETD"] = departure
            df.at[idx, "ETA"] = earliest_departure

    return df.to_dict(orient="records")

print(allocation(None))