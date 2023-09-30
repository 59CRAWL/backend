from datetime import datetime

""""
Begin
"""
# Create queues
#   1 for each berth that is being used
#       Data that should be populated with should look like [EDT, EDT, EDT, ...]
berths = 10 * [-1]

print(berths)

# 1. Call Machine Learning model with a CSV file
# Important stuff that Raymond will spit out
#   Expected Arrival Time & Expected Departure Time

# 2. Sort the ships by Expected Arrival Time
data = ["some csv"]

# 3. Loop through the arrival times
for ship in data:
    # Look through the berths if they are filled
    for i in range(len(berths)):
        berth = berths[i]
        
        # Kick out ship once its passed EDT
        if datetime.now() > berth:
            berth = -1

        # Find the first non-filled berth and allocate the ship to it
        if berth == -1:
            # Also, update the expected departure time of the ship
            # Remember to modify the model with what berth number it is
            berth = {ship: "Expected Departure Time"}



# NOTE: Should we target the idea of having a ship waiting, but no berths open?
