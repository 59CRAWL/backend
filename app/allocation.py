
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

def allocation(df):
    # """
    # Testing data for user
    # """
    # data = [{"shipId": 1, "ETA": datetime.datetime.now(),"PTD": datetime.datetime.now() + datetime.timedelta(days=7)}, 
    #         {"shipId": 2, "ETA": datetime.datetime.now() - datetime.timedelta(days=7), "PTD": datetime.datetime.now() + datetime.timedelta(days=1)},
    #         {"shipId": 1, "ETA": datetime.datetime.now(),"PTD": datetime.datetime.now() + datetime.timedelta(days=7)}, 
    #         {"shipId": 2, "ETA": datetime.datetime.now() - datetime.timedelta(days=7), "PTD": datetime.datetime.now() + datetime.timedelta(days=1)}]

    # df = pd.DataFrame.from_dict(data)

    # Sort the ships by Expected Arrival Time
    df.sort_values(by="ETA", inplace=True)

    # Insert expected added values later
    df["Berth"] = 0
    df["As Scheduled"] = None

    # Creating queues, 1 for each berth that exists
    #   Data that should be populated with should look like [PTD, PTD, PTD, ...]
    berths = [Queue() for _ in range(berth_count)]

    # Loop through ship arrival times
    for idx, ship in df.iterrows():
        arrival = ship.get("ETA")
        departure = ship.get("PTD")
        on_time = False

        # Loop through the berths to find empty berths
        for i in range(len(berths)):
            berth = berths[i]

            # Kick out ships once PTDs have passed
            for PTD in berth.items:
                if PTD < arrival:
                    berth.dequeue()
                else:
                    break

            # Allocate a ship to empty berth
            if berth.is_empty():
                # Update berth with PTD and update ship details
                berth.enqueue(departure)
                df.at[idx, "Berth"] = i
                df.at[idx, "As Scheduled"] = 0
                on_time = True
                break
        
        # If berths are full, indicate new docking time if necessary
        if not on_time:
            # Find the earliest PTD for the docks
            earliest_departure = datetime.datetime.max
            next_berth = -1
            for index, berth in enumerate(berths):
                PTD = berth.get_last()
                if PTD < earliest_departure:
                    earliest_departure = PTD
                    next_berth = index
            
            # Update berth and scheduled or affected as accordingly
            df.at[idx, "Berth"] = next_berth
            df.at[idx, "As Scheduled"] = 1

            # Calculate the updated estimated departure time and adjust in the sheets
            departure += earliest_departure - arrival
            berths[next_berth].enqueue(departure)
            df.at[idx, "PTD"] = departure
            df.at[idx, "ETA"] = earliest_departure

    return df.to_dict(orient="records")