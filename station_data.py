from urllib2 import urlopen
from datetime import date, datetime
from urllib import urlencode
#from pylab import plot, show
import os, sys
import urllib2
import json
import pandas
from pprint import pprint
from StringIO import StringIO
from numpy import genfromtxt

def extract_station_data(code):
    url = "http://data.hisparc.nl/api/station/%d/"%(code)
    try:
        response = json.loads(urllib2.urlopen(url).read())
    except urllib2.HTTPError:
        return None
    else:
        return response

def get_stations():
    data = []
    url = 'http://data.hisparc.nl/api/stations'
    response = json.loads(urllib2.urlopen(url).read())
    for station in response:
        data.append(station['number'])
    return data

def get_events(station, start, end):
    url = 'http://data.hisparc.nl/data/'+str(station)+'/events'
    query = urlencode({'download': False, 'start': start,'end': end})
    full_url = url + '?' + query
    data = urlopen(full_url).read()
    format = [('date', 'datetime64[D]'), ('time', '|S8'),
              ('timestamp', 'int'), ('nanoseconds', 'int'),
              ('pulseheights', '4int16'), ('integrals', '4int32'),
              ('n1', 'float32'), ('n2', 'float32'),
              ('n3', 'float32'), ('n4', 'float32'),
              ('t1', 'float32'), ('t2', 'float32'),
              ('t3', 'float32'), ('t4', 'float32'),
              ('t_trigger', 'float32')]
    a = genfromtxt(StringIO(data), delimiter="\t", dtype=format)
    return a

def eventToJSON(event, station_data):
    tempDict = {'timestamp': event[2],
                'nanoseconds': event[3], 'altitude': station_data['altitude'],
                'latitude': station_data['latitude'], 'longitude': station_data['longitude']}
    return tempDict

def eventToTxt(event):
    with open("./dataStore/"+str(event["timestamp"])+str(event["nanoseconds"])+".cosmic", "w") as outfile:
        json.dump(event, outfile, sort_keys = True, indent = 4)
    outfile.close()

def txtToEvent(fileTarget):
    with open(fileTarget) as inputFile:
        return json.load(inputFile)

def coincidenceCheck(listOfEvents, coincidenceRequirement):
    """
    :param listOfEvents:
    :param coincidenceRequirement:
    :return: from listOfEvents returns a subset that meet coincidence requirements
     If multiple subsets are found return list of events
    """
    return

class Event:
    def __init__(self, eventInput):
        """
        Initiate event parameters from data source. Default data for all events is spatial data,
        time stamp and more accurate count depending on device. Further data may be added as required
        in subclass for device
        """
        Event.lat = eventInput["latitude"]
        Event.lon = eventInput["longitude"]
        Event.alt = eventInput["altitude"]
        Event.timestamp = eventInput["timestamp"]
        Event.nanosecond = eventInput["nanseconds"]






def main():
    # try:
    #     os.mkdir("./dataStore/")
    # except:
    #     pass
    # station_ids = [3,5,6] #get_stations()
    # for code in station_ids:
    #     outputStation = extract_station_data(code)
    #     if outputStation is not None:
    #         pprint(outputStation)
    #     eventOutput = get_events(code,datetime(2013, 7, 2, 11, 0),datetime(2013, 7, 2, 11, 05))
    #     for event in eventOutput:
    #         eventData =  eventToJSON(event, outputStation)
    #         eventToTxt(eventData)

    eventListing = []
    for storFile in os.listdir(os.getcwd()+"/dataStore/"):
        if storFile.endswith(".cosmic"):
            eventListing.append(txtToEvent(os.getcwd()+"/dataStore/"+storFile))




if __name__ == '__main__':
    main()
