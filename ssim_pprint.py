import argparse
import logging
import os
import sys

from utils import convert_to_text

# Set the log output file and log level.
logging.basicConfig(filename="ssim_pprint.log", level=logging.DEBUG)


def make_parser():
    """ Construct the command line parser """
    logging.debug("Constructing command line parser...")
    description = "Display information about a specific Airline Flight"
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(dest="command",
                                       help="Available Commands")

    #Todo: Consider supporting a mapping of names to IATA codes.
    logging.debug("Constructing carrier subparser")
    carrier_parser = subparsers.add_parser("carrier", help="")
#    carrier_parser.add_argument("code", help="Two digit IATA carrier code.")
#    carrier_parser.add_argument("flight", help="The flight number to look up.")
    carrier_parser.add_argument("filename", help="Name of the file to search.")

    return parser

def main():
    """ Main function """
    logging.info("Starting the SSIM pretty printer.")
    parser = make_parser()
    logging.debug("All arguments are: {!r}".format(sys.argv[0:]))
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary

    arguments = vars(arguments)
    logging.debug("Arguments are now: {!r}".format(arguments))
    command = arguments.pop("command")
    # Log an error and quit if file doesn't exist
    if os.path.exists(arguments['filename']):
        logging.debug("File {!r} exists - Continuing.".format(
                arguments['filename']))
    else:
        logging.debug("File {!r} doesn't exist.  Exiting.".format(
                arguments['filename']))
        sys.exit("SSIM file name provided not found.")

    if command == "carrier":
        file_to_parse = convert_to_text(arguments['filename'])
        print("Check file {!r}".format(file_to_parse))


if __name__ == "__main__":
    main()
