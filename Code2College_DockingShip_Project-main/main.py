#Main.py 
import dockingBays as db
from datetime import datetime
from collections import defaultdict #using dateTime for comparissons 

# helps to run through the time strings
def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

# this function checks if a shcedule is available to bay
def available_schedule(bay, arrival_time, departure_time):
    arrival_time = parse_time(arrival_time)
    departure_time = parse_time(departure_time)
    for scheduled in bay['schedule']:
        scheduled_arrival = parse_time(scheduled[0])
        scheduled_departure = parse_time(scheduled[1])
        if arrival_time < scheduled_departure and departure_time > scheduled_arrival:
            return False
    return True

# organization
bays_by_size = defaultdict(list)
for bay in db.docking_bays:
    bays_by_size[bay['size']].append(bay)

# find the bays available for current shipp
def find_available_bays(ship_size, arrival_time, departure_time):
    available_bays = []
    for bay in bays_by_size[ship_size]:
        if available_schedule(bay, arrival_time, departure_time):
            available_bays.append(bay)
    return available_bays

# assing the current ship to bay
def assigning_ships(incoming_ships):
    incoming_ships = sorted(incoming_ships, key=lambda x: parse_time(x['arrival_time']))
    for ship in incoming_ships:
        ship_size = ship['size']
        arrival_time = ship['arrival_time']
        departure_time = ship['departure_time']
        available_bays = find_available_bays(ship_size, arrival_time, departure_time)
       
        if available_bays:
            selected_bay = available_bays[0]
            selected_bay['schedule'].append((arrival_time, departure_time, ship['ship_name']))
            print(f"Assigned {ship['ship_name']} to Bay {selected_bay['bay_id']}")
        else:
            print(f"No bays available for {ship['ship_name']}.")

# docking info
def print_docking_bays():
    print("Docking Bays:")
    for bay in db.docking_bays:
        print(f"Bay {bay['bay_id']} - Size: {bay['size']}, Schedule: {bay['schedule']}")

# ships incomming info
def print_incoming_ships():
    print("\nIncoming Ships:")
    for ship in db.incoming_ships:
        print(f"Ship {ship['ship_name']} - Size: {ship['size']}, Arrival: {ship['arrival_time']}, Departure: {ship['departure_time']}")

# Main function
def main():
    print_docking_bays()
    print_incoming_ships()
   
    print("\nAssigning Ships to Bays...")
    assigning_ships(db.incoming_ships)
   
    print("\nUpdated Docking Bays:")
    print_docking_bays()

if __name__ == "__main__":
    main()
