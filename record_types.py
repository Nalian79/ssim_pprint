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
        self.name = self.carrier_code + "_record_two"

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
        self.name = self.carrier_code + self.flight + "_record_three"

    def prettyprint(self):
        print "Printing out data for " + self.name
        print "Carrier code: " + self.carrier_code
        print "Flight number: " + self.flight
        print "End of " + self.name

class RecordFour(object):
    """ Parse an SSIM record four entry """

    def __init__(self, line):
        self.carrier_code = line[2:5]
        self.flight = line[5:9]
        self.name = self.carrier_code + self.flight + "_record_four"

    def prettyprint(self):
        print "Printing out data for " + self.name
        print "Carrier code: " + self.carrier_code
        print "Flight Number: " + self.flight
        print "Done printing data for " + self.name
