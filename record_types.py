import os
import re

class RecordTwo(object):
    """Parse an SSIM record two entry. """

    def __init__(self, line):
        self.time_mode = line[1].strip()
        self.carrier_code = line[2:5].strip()
        self.validity_period = line[14:28].strip()
        self.creation_date = line[28:35].strip()
        self.sell_date = line[64:71].strip()
        self.secure_flight = line[168].strip()
        self.eticket = line[188:190].strip()
        self.name = self.carrier_code + "_r2"

    def prettyprint(self):
        """ Convert variables and pretty print the data from this record """
        if self.time_mode == 'L':
            time = "Local"
        else:
            time = "UTC"
        validity_period_start = self.validity_period[0:7]
        validity_period_end = self.validity_period[7:]
        print "Printing out data for " + self.name
        print "Schedule time mode for this file is: " + time
        print "Carrier Code: " + self.carrier_code
        print "Created on: " + str(self.creation_date)
        if self.sell_date !='':
            print "Schedules are open for sale on: " + self.sell_date
        print "Schedules Start Date: " + validity_period_start
        print "Schedules End Date: " + validity_period_end
        if self.eticket == "ET":
            print "Flights contained in this file are e-ticketable by default"
        print "End of " + self.name


class RecordThree(object):
    """ Parse an SSIM record three entry """

    def __init__(self, line):
        self.carrier_code = line[2:5]
        self.flight = line[5:9]
        self.ivi = line[9:11] # Itinerary Variation Identifier
        self.leg_sequence = line[11:13]
        self.service_type = line[13]
        self.period_of_operation_start = line[14:21]
        self.period_of_operation_end = line[21:28]
        self.days_of_operation = line[28:35]
        self.frequency_rate = line[35]
        self.departure_station = line[36:39]
        self.passenger_std = line[39:43] # Passenger Scheduled Time Departure
        self.aircraft_std = line[43:47] # Aircraft Scheduled Time Departure
        self.departure_utc_variation = line[47:52] # UTC variation for origin
        self.passenger_departure_terminal = line[52:54]
        self.arrival_station = line[54:57]
        self.aircraft_sta = line[57:61] # Aircraft Scheduled Time Arrival
        self.passenger_sta = line[61:65] # Passenger Scheduled Time Arrival
        self.arrival_utc_variation = line[65:70] # UTC variation for destination
        self.passenger_arrival_terminal = line[70:72]
        self.aircraft_type = line[72:75]
        self.prdb = line[75:95] # Passenger Reservations Booking Designator
        self.prbm = line[95:100] # Passenger Reservations Booking Modifier
        self.meal_service = line[100:110]
        self.joint_airline_designator = line[110:119]
        self.mct = line[119:120] # Minimum Connection Time
        self.secure_flight = line[121] # Secure Flight Indicator
        self.ivi_overflow = line[127] # Itinerary Variation Overflow
        self.aircraft_owner = line[128:131]
        self.cockpit_crew = line[131:134]
        self.cabin_crew = line[134:137]
        self.onward_airline = line[137:139]
        self.onward_flight = line[140:143]
        self.disclosure = line[148] # Operating Airline disclosure - DEI 2
        self.traffic_restriction = line[149:160]
        self.aircraft_configuration = line[172:192]
        self.date_variation = line[192:194]
        self.record_serial_number = line[194:200]
        self.name = self.carrier_code + self.flight + self.ivi + "_r3"

    def prettyprint(self):
        print "Printing out data for " + self.name
        print "Carrier code: " + self.carrier_code
        print "Flight number: " + self.flight
        print "Variation number: " + self.ivi
        print "Leg Sequence Number: " + self.leg_sequence
        print "Depart: " + self.departure_station + " At: " + self.passenger_std
        print "Arrive: " + self.arrival_station + " At: " + self.passenger_sta
        print "End of " + self.name

class RecordFour(object):
    """ Parse an SSIM record four entry """

    def __init__(self, line):
        self.carrier_code = line[2:5]
        self.flight = line[5:9]
        self.ivi = line[9:11]
        self.leg_sequence = line[11:13]
        self.service_type = line[13]
        self.board_point_indicator = line[18:29]
        self.off_point_indicator = line[29]
        self.dei = line[30:33] # Data Element Identifier
        self.segment = line[33:39]
        self.board_point = line[33:36]
        self.off_point = line[36:39]
        self.dei_data = line[40:194]
        self.name = self.carrier_code + self.flight + self.ivi + "_r4"

    def prettyprint(self):
        print "Printing out data for " + self.name
        print "Carrier code: " + self.carrier_code
        print "Flight Number: " + self.flight
        print "Variation number: " + self.ivi
        print "Leg Sequence Number: " + self.leg_sequence
        print "DEI " + self.dei
        print "Origin: " + self.board_point
        print "Destination: " + self.off_point
        print "DEI Data: " + self.dei_data
        print "Done printing data for " + self.name
