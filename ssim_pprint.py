import argparse
import logging
import os
import re
import sys

from flight_classes import RecordTwo, RecordThree, RecordFour, Flight
from utils import is_file_compressed, uncompress

# Set the log output file and log level.
logging.basicConfig(filename='ssim_pprint.log', level=logging.DEBUG)


def parse_records(carrier, filename):
    """Read an SSIM file, then call record type parsers to fill in data.

    Args:
      carrier: str. Two character IATA code for Airline Carrier
      filename: Str. The file to parse
    Returns:
      A tuple of dictionary objects.  Each dictionary contains record objects.
    """

    carrier_regex = '^2.' + carrier.upper()
    leg_regex = '^3.' + carrier.upper()
    seg_regex = '^4.' + carrier.upper()
    carrier_record = []
    leg_records = []
    seg_records = []
    my_rec_two = ''
    with open(filename, 'rb') as f:
        for line in f:
            if re.search(carrier_regex, line):
                carrier_record.append(RecordTwo(line))
            if re.search(leg_regex, line):
                leg_records.append(RecordThree(line))
            if re.search(seg_regex, line):
                seg_records.append(RecordFour(line))
        return carrier_record, leg_records, seg_records


def create_flights(carrier_record, record_list, flights):
    """Create unique flight objects from a list of record objects.

    Args:
      carrier_record: A record2 object for the carrier
      record_list: List of record objects obtained via parsing an SSIM file.
      flights: dict. A dictionary object to put flight objects into.
    Returns:
      flights: dict. Mapping of flight names to flight objects.
    """
    for record in record_list:
        flightname = record.carrier_code + record.flight
        flightname = flightname.replace(" ", "")
        if not flightname in flights:
            flights[flightname] = Flight(record.carrier_code,
                                         record.flight, carrier_record)
    return flights


def update_flights(record_list, flights):
    """Update flight objects with information from record objects.

    Args:
      records: list.  List of record objects obtained via parsing an SSIM file.
      flights: dict.  A dictionary of flight objects to update.
    returns:
      flights: dict. Updated dictionary of flight objects.
 """
    for record in record_list:
        flightname = record.carrier_code + record.flight
        flightname = flightname.replace(" ", "")
        if flightname in flights:
            flightobj = flights[flightname]
            flightobj.create_variation(record.ivi, record)
    return flights


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
        carrier = args['carrier']
        if is_file_compressed(filename):
            file_to_parse = uncompress(filename)
        else:
            file_to_parse = filename
            pass
        print("SSIM file {!r} now uncompressed".format(file_to_parse))
        # parse the file into record objects
        record2s, record3s, record4s = parse_records(carrier, file_to_parse)
        # create a record name to match records to
        carrier_record_name = carrier + "_r2"
        for record in record2s:
            if record.name == carrier_record_name:
                carrier_record = record
        # Create a dictionary for keeping track of flight objects
        flights = {}
        create_flights(carrier_record, record3s, flights)
        update_flights(record3s, flights)

        for k in flights:
            print flights[k].name, flights[k].flight_num, flights[k].ivi


if __name__ == "__main__":
    main()
