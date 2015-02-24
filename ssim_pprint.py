import argparse
import logging
import os
import re
import sys

from record_types import RecordTwo, RecordThree, RecordFour
from utils import is_file_compressed, uncompress

# Set the log output file and log level.
logging.basicConfig(filename='ssim_pprint.log', level=logging.DEBUG)


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
