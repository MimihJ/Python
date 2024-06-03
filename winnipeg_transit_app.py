""" 
Winnipeg Transit App Assignment
Hyeryung Jin 
2024 Jan 14
"""




from requests import get
from dateutil.parser import parse
from colorama import init, Fore, Style

# Set up colorama for colored output
init(autoreset=True)

API_KEY = "KFAK3KkTuQrp9AKOVt79"
lon = -97.1375  # GPS longitude of location
lat = 49.86912  # GPS latitude of location
distance = 300  # radius in meters to search around GPS coordinates

# URL to request stops
url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"

# Request bus stops nearby
resp_stops = get(url_stops).json()

def fetch_arrival_times(stop_key, api_key):
    # Modify the URL based on the selected bus stop
    url_arrivals = f"https://api.winnipegtransit.com/v3/stops/{stop_key}/schedule.json?api-key={API_KEY}"

    # Request arrival times for the selected bus stop
    resp_arrivals = get(url_arrivals).json()

    return resp_arrivals

def display_colored_time(arrival_time, scheduled_time):
    arrival_datetime = parse(arrival_time)
    scheduled_datetime = parse(scheduled_time)

# Compare scheduled and estimated arrival times
    if arrival_datetime == scheduled_datetime:
        print(Fore.GREEN + f"Predicted: {arrival_datetime.strftime('%H:%M:%S')}, Scheduled: {scheduled_datetime.strftime('%H:%M:%S')}" + Style.RESET_ALL)
    elif arrival_datetime > scheduled_datetime:
        print(Fore.RED + f"Predicted: {arrival_datetime.strftime('%H:%M:%S')}, Scheduled: {scheduled_datetime.strftime('%H:%M:%S')}" + Style.RESET_ALL)
    else:
        print(Fore.BLUE + f"Predicted: {arrival_datetime.strftime('%H:%M:%S')}, Scheduled: {scheduled_datetime.strftime('%H:%M:%S')}" + Style.RESET_ALL)

# Display bus stops
print("Bus Stops:")
for stop in resp_stops['stops']:
    print(f"{stop['key']}: {stop['name']}")

# Ask the user to choose a bus stop
selected_stop = input("Enter the key of the bus stop you want to check: ")

# Fetch arrival times for the selected bus stop
resp_arrivals = fetch_arrival_times(selected_stop, API_KEY)

# Display arrival times with color coding
print("\nArrival Times (green = on_time, red= late, blue = early):")

# Check if 'route-schedules' key exists in the response
if 'route-schedules' in resp_arrivals['stop-schedule']:
    # Iterate through each route
    for route_schedule in resp_arrivals['stop-schedule']['route-schedules']:
        # Iterate through scheduled stops for the route
        for scheduled_stop in route_schedule.get('scheduled-stops', []):
            predicted_arrival = scheduled_stop['times']['arrival']['estimated']
            scheduled_arrival = scheduled_stop['times']['arrival']['scheduled']
            
            
            display_colored_time(predicted_arrival, scheduled_arrival)

else:
    print("No arrival times available for the selected bus stop.")
