from json import loads
from requests import get                # pip3 install requests
from argparse import ArgumentParser
from datetime import datetime


# ---------------- Converting data time format to unix timestamp for use in api -----------------

def dt_to_timestamp(date, time):
    dt = date + ' ' + time
    dt_obj = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
    timestamp = dt_obj.timestamp()
    return timestamp


# ---------------- Command -----------------

parser = ArgumentParser(
    prog='python3 satellite.py',
    description="A command for getting location, in latitude and longitude or country code and zone, at real-time or "
                "a specific time",
    epilog="Find out more on GitHub: https://github.com/honey-py/ccBackendTask1"
)

parser.add_argument('id', type=str, help='The ID of the satellite whose location is being requested')
parser.add_argument('date', default="-1", type=str, nargs="?",
                    help='The date on which you want to find the location (optional, '
                         'if you want to know location on a specific date and time)')
parser.add_argument('time', default="-1", type=str, nargs="?",
                    help='The time at which you want to find the location (optional, '
                         'if you want to know location on a specific date and time)')
parser.add_argument('-l', '--location', action='store_true',
                    help='Return the location in longitude and latitude format')
parser.add_argument('-c', '--country', action='store_true',
                    help='Return the location in country code and time zone format')

args = parser.parse_args()

# ---------------- Requesting, reading json and printing location -----------------

if args.date == "-1" or args.time == "-1":
    data = loads(get(f"https://api.wheretheiss.at/v1/satellites/{args.id}").text)
    latitude = data["latitude"]
    longitude = data["longitude"]
else:
    data = loads(get(
        f"https://api.wheretheiss.at/v1/satellites/{args.id}/positions?timestamps={dt_to_timestamp(args.date, args.time)}").text)
    latitude = data[0]["latitude"]
    longitude = data[0]["longitude"]

if args.location or (not args.country and not args.location):
    print("Longitude: ", longitude)
    print("Latitude: ", latitude)

if args.country or (not args.country and not args.location):
    cdata = loads(get(
        f"https://api.wheretheiss.at/v1/coordinates/{longitude},{latitude}").text)
    if 'error' in cdata:
        print("This location most likely doesn't have any timezone and country_code")
    else:
        print("Country Code: ", cdata["country_code"])
        print("Time Zone: ", cdata["timezone_id"])
