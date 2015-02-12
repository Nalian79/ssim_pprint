import argparse
import logging
import os
import sys

from utils import is_file_compressed, uncompress

# Set the log output file and log level.
logging.basicConfig(filename='ssim_pprint.log', level=logging.DEBUG)


def make_parser():
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
    parser = make_parser()
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
            sis.exit('SSIM file name provided not found.')

        filename = args['ssim']
        if is_file_compressed(filename):
            file_to_parse = uncompress(filename)
        else:
            file_to_parse = filename
            pass
        print("Check file {!r}".format(file_to_parse))


if __name__ == "__main__":
    main()
