import argparse
import logging
import os
import re
import sys

from record_types import RecordTwo, RecordThree, RecordFour
from utils import is_file_compressed, uncompress

# Set the log output file and log level.
logging.basicConfig(filename='ssim_pprint.log', level=logging.DEBUG)

def make_recordtwo_dict(line):
    """Create a dictionary from an SSIM record 2. """
    carrier_dict = {
        'time_mode' : line[1],
        'carrier_code' : line[2:5],
        'validity_period' : line[14:28],
        'creation' : line[28:35],
        'sell_date' : line[64:71],
        'secure_flight' : line[168],
        'eticket' : line[188:190]
        }
    return carrier_dict


def make_recordthree_dict(line):
    leg_dict = {
        'carrier_code' : line[2:5], # Two character IATA airline code
        'flight_num' : line[5:9],
        'ivi' : line[9:11], # Itinerary Variation Identifier
        'leg_seq' : line[11:13], # Leg Sequence Number
        'service_type' : line[13], # Passenger, Cargo, Mail, etc
        'period_of_op_start' : line[14:21],
        'period_of_op_end' : line[21:28],
        'days_of_op' : line[28:35], # Days of operation
        'freq_rate' : line[35], # Frequency rate
        'departure_station' : line[36:39],
        'passenger_std' : line[39:43], # Schedule time of Passenger departure
        'aircraft_std' : line[43:47], # Scheduled time of Aircraft departure
        'dep_utc_variation' : line[47:52], # UTC variation for origin
        'pass_dterm' : line[52:54], # Passenger Terminal for depature
        'arrival_station' : line[54:57],
        'air_sta' : line[57:61], # Aircraft scheduled time of Arrival
        'pass_sta' : line[61:65], # Passenger scheduled time of Arrival
        'arr_utc_variation' : line[65:70], # UTC variation for destination
        'pass_aterm' : line[70:72], # Passenger arrival terminal
        'aircraft_type' : line[72:75], # Type of aircraft
        'prdb' : line[75:95], # Passenger Reservations Booking Designator
        'prbm' : line[95:100], # passenger reservations booking modifier
        'meal_service' : line[100:110],
        'mct' : line[119:120], # Minimum Connection Time
        'secure_flight' : line[121], # Secure flight indicator
        'ivi_overflow' : line[127],
        'aircraft_owner' : line[128:131],
        'cockpit_crew' : line[131:134],
        'cabin_crew' : line[134:137],
        'onward_airline' : line[137:140], # Airline Designator
        'onward_flight_num' : line[140:144],
        'disclosure' : line[148], # operating airline disclosure - DEI 2
        'traffic_restriction' : line[149:160],
        'aircraft_configuration' : line[172:192],
        'date_variation' : line[192:194],
        'record_serial_num' : line[194:]
        }
    return leg_dict


def make_recordfour_dict(line):
    seg_dict = {
        'op_suffix' : line[1],
        'carrier_code' : line[2:5],
        'flight_num' : line[5:9],
        'ivi' : line[9:11],
        'leg_seq' : line[11:13],
        'service_type' : line[13],
        'board_point_indicator' : line[18:29],
        'off_point_indicator' : line[29],
        'dei' : line[30:33],
        'seg' : line[33:39],
        'board_point' : line[33:36],
        'off_point' : line[36:39],
        'dei_data' : line[40:194],
        'record_serial_number' : line[194:]
        }
    return seg_dict


def parse_records(carrier, filename):
    """Read an SSIM file, then call record type parsers to fill in data.

    Args:
      carrier: str. Two character IATA code for Airline Carrier
      filename: Str. The file to parse
    Returns:
      A tuple of record objects
    """

    carrier_regex = '^2.' + carrier.upper()
    leg_regex = '^3.' + carrier.upper()
    seg_regex = '^4.' + carrier.upper()
    carrier_record = []
    leg_record = []
    seg_record = []
    my_rec_two = ''
    with open(filename, 'rb') as f:
        for line in f:
            if re.search(carrier_regex, line):
                carrier_record.append(RecordTwo(line))
            if re.search(leg_regex, line):
                leg_record.append(RecordThree(line))
            if re.search(seg_regex, line):
                seg_record.append(RecordFour(line))
        return carrier_record, leg_records, seg_records


def combine_records(record_list):
    """Compress multiple record objects dealing with 1 flight into one object
    """
    # Need an object to store the final compressed record in
    for records in record_list:
        # if the record.name is new, store it in the final object
        # if record.name is present in the final object, then move on
        # to other record parts.  For each unique part, store it in the
        # final object - discard repeats.


def parse_commands():
    """ Construct the command line parser."""

    logging.debug('Constructing command line parser...')
    description = 'Display information about a specific Airline Flight'
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(dest='command',
                                       help='Available Commands')

    #Todo: Consider supporting a mapping of names to IATA codes.
    logging.debug('Constructing the flight lookup subparser')
    lookup_parser = subparsers.add_parser('lookup',
                                          help='Look up specific flight data.')
    lookup_parser.add_argument('-c', '--carrier',
                               help='Two digit IATA carrier code')
    lookup_parser.add_argument('-f', '--flight',
                               help='Number of the flight to lookup')
    lookup_parser.add_argument('-s', '--ssim',
                               help='Name of the SSIM file to search')
    return parser


def main():
    """ Parse command line args, take action based on arguments."""

    logging.info("Starting the SSIM pretty printer.")
    parser = parse_commands()
    logging.debug("All arguments are: {!r}".format(sys.argv[0:]))
    args = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary

    args = vars(args)
    logging.debug("Arguments are now: {!r}".format(args))
    command = args.pop("command")
    # Log an error and quit if file doesn't exist

    if command == "lookup":
        if os.path.exists(args['ssim']):
            logging.debug('File {!r} exists, Continuing.'.format(
                    args['ssim']))
        else:
            logging.debug('File {!r} doesn\'t exist.  Exiting'.format(
                    arguments['ssim']))
            sys.exit('SSIM file name provided not found.')

        filename = args['ssim']
        if is_file_compressed(filename):
            file_to_parse = uncompress(filename)
        else:
            file_to_parse = filename
            pass
        print("Check file {!r}".format(file_to_parse))



if __name__ == "__main__":
    main()
