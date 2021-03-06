import os
import re

class RecordTwo(object):
    """Parse an SSIM record two entry. """

    def __init__(self, line):
        self.original_record = line
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
        self.original_record = line
        self.carrier_code = line[2:5].strip()
        self.flight = line[5:9].strip()
        self.ivi = line[9:11].strip() # Itinerary Variation Identifier
        self.leg_sequence = line[11:13].strip()
        self.service_type = line[13].strip()
        self.period_of_operation_start = line[14:21].strip()
        self.period_of_operation_end = line[21:28].strip()
        self.days_of_operation = line[28:35].strip()
        self.frequency_rate = line[35].strip()
        self.departure_station = line[36:39].strip()
        self.passenger_std = line[39:43].strip()
        self.aircraft_std = line[43:47].strip()
        self.departure_utc_variation = line[47:52].strip()
        self.passenger_departure_terminal = line[52:54].strip()
        self.arrival_station = line[54:57].strip()
        self.aircraft_sta = line[57:61].strip()
        self.passenger_sta = line[61:65].strip()
        self.arrival_utc_variation = line[65:70].strip()
        self.passenger_arrival_terminal = line[70:72].strip()
        self.aircraft_type = line[72:75].strip()
        self.prdb = line[75:95].strip() # Booking Designator
        self.prbm = line[95:100].strip() # Booking Modifier
        self.meal_service = line[100:110].strip()
        self.joint_airline_designator = line[110:119].strip()
        self.mct = line[119:120].strip()
        self.secure_flight = line[121].strip() # Secure Flight Indicator
        self.ivi_overflow = line[127].strip() # Itinerary Variation Overflow
        self.aircraft_owner = line[128:131].strip()
        self.cockpit_crew = line[131:134].strip()
        self.cabin_crew = line[134:137].strip()
        self.onward_airline = line[137:139].strip()
        self.onward_flight = line[140:143].strip()
        self.disclosure = line[148].strip() # DEI 2
        self.traffic_restriction = line[149:160].strip()
        self.traffic_restriction_overflow = line[160]
        self.aircraft_configuration = line[172:192].strip()
        self.date_variation = line[192:194].strip()
        self.record_serial_number = line[194:200].strip()
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
        self.original_record = line
        self.carrier_code = line[2:5].strip()
        self.flight = line[5:9].strip()
        self.ivi = line[9:11].strip()
        self.leg_sequence = line[11:13].strip()
        self.service_type = line[13].strip()
        self.board_point_indicator = line[18:29].strip()
        self.off_point_indicator = line[29].strip()
        self.dei = line[30:33].strip() # Data Element Identifier
        self.segment = line[33:39].strip()
        self.board_point = line[33:36].strip()
        self.off_point = line[36:39].strip()
        self.dei_data = line[39:194].strip()
        self.record_serial_number = line[194:]
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


class Flight(object):
    """An object that represents all information for a single flight.

    Each flight will have one or more variations on it's schedule.  The Flight
    class uses the FlightVariation class to create objects for each schedule
    variation.  The Flight class maintains a list of those variations associated
    with the flight in a dictionary.
    """

    def __init__(self, carrier_code, flight_num, carrier_record):
        self.name = carrier_code + flight_num
        self.carrier_code = carrier_code
        self.flight_num = flight_num
        self.ivi = {}
        self.handle_record2(carrier_record)

    def handle_record2(self, carrier_record):
        """Update Flight object with carrier record information """
        self.time_mode = carrier_record.time_mode
        self.validity_period = carrier_record.validity_period
        self.valid_start = carrier_record.validity_period[:7]
        self.valid_end = carrier_record.validity_period[7:]
        self.release_date = carrier_record.sell_date
        self.secure_flight = carrier_record.secure_flight

    def create_variation(self, ivi, record):
        """ Create an initial flight variation."""
        if not ivi in self.ivi:
            # Send this to the FlightVariation class
            self.ivi[ivi] = FlightVariation(self.flight_num, ivi, record)
        return self.ivi


class FlightVariation(object):
    """An object that represents all information for a single flight variation.

    Each flight variation can have one or more legs, and multiple DEIs
    associated with it.
    """

    def __init__(self, flight_num, ivi, record):
        self.name = flight_num + ivi
        self.legs = {}
        self.legs
        self.update_variation(record)

    def update_variation(self, record):
        if not record.leg_sequence in self.legs:
            self.legs[record.leg_sequence] = {}
        leg = self.legs[record.leg_sequence]
        for key in vars(record):
            value = getattr(record, key)
            if key == 'dei':
                leg['deis'] = {}
                leg['deis'][key] = value
            if value != '' and key != 'original_record':
                leg[key] = value
        return self.legs

