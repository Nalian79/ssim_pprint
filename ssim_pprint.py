import argparse
import logging
import os
import re
import sys

from utils import is_file_compressed, uncompress

# Set the log output file and log level.
logging.basicConfig(filename='ssim_pprint.log', level=logging.DEBUG)

def parse_record_two(line):
    """Create a dictionary from an SSIM record 2. """
    carrier_dict = {
        'time_mode' : line[1],
        'carrier_code' : line[2:4],
        'validity_period' : line[14:27],
        'creation' : line[28:34],
        'sell_date' : line[64:70],
        'secure_flight' : line[168],
        'eticket' : line[188:189]
        }
    return carrier_dict


def parse_record_three(line):
    leg_dict = {
        'carrier_code' : line[2:4],
        'flight_num' : line[5:8],
        'ivi' : line[9:10],
        'leg_seq' : line[11:12],
        'service_type' : line[13],
        'period_of_op' : line[14:27],
        'days_of_op' : line[28:34],
        'dep_station' : line[36:38],
        'pass_std' : line[39:42],
        'pass_dterm' : line[52:53],
        'arr_station' : line[54:56],
        'pass_sta' : line[61:64],
        'utc_variation' : line[65:79],
        'pass_aterm' : line[70:71],
        'aircraft_type' : line[72:74],
        'mct' : line[119:120],
        'secure_flight' : line[121],
        'airline_des' : line[137:139],
        'fnum' : line[140:143]
        }
    return leg_dict


def parse_record_four(line):
    seg_dict = {
        'op_suffix' : line[1],
        'carrier_code' : line[2:4],
        'flight_num' : line[5:8],
        'ivi' : line[9:10],
        'leg_seq' : line[11:12],
        'service_type' : line[13],
        'board_point_indicator' : line[18:28],
        'off_point_indicator' : line[29],
        'dei' : line[30:32],
        'seg' : line[33:38],
        'board_point' : line[33:35],
        'off_point' : line[36:38],
        'dei_data' : line[40:194],
        }
    return seg_dict


def parse_file(carrier, filename):
    """Read an SSIM file, then call record type parsers to fill in data.

    Args:
      carrier: str. Two character IATA code for Airline Carrier
      filename: Str. The file to parse
    Returns:
      Once I know what I'm returning fill this in.
    """

    carrier_regex = r'^2.' + carrier
    carrier_record = {}
    leg_record = {}
    seg_record = {}
    with open(filename, 'rb') as f:
        for line in f:
            if re.search(carrier_regex, line):
#                carrier_record = parse_record_two(line)
                carrier_record.update(parse_record_two(line))
            elif re.search('^3', line):
                leg_record = parse_record_three(line)
            elif re.search('^4', line):
                seg_record = parse_record_four(line)
            return carrier_record, leg_record, seg_record


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
