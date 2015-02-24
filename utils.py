import gzip


def is_file_compressed(filename):
    """ Determine if the file we are dealing with is compressed with gzip.

    Args:
      filename: name of the file to check.
    Returns:
      A string indicating the type of file.
    """

    magic_dict = {
        "\x1f\x8b\x08": "gz",
        "\x50\x4b\x03\x04": "zip"
        }

    max_len = max(len(x) for x in magic_dict)

    with open(filename) as f:
        file_start = f.read(max_len)
        for magic, filetype in magic_dict.items():
            if file_start.startswith(magic):
                return True, filetype
        return False


def uncompress(filename):
    """Uncompress the gzipped file, return the uncompressed file name.

    Read in the compressed file, and write out a new file, uncompressed,
    with the same name, minus .gz.

    args: gzfilename - the name of the gzipped file you want to uncompress.
    """

    print('Incoming file is {!r}'.format(filename))
    if is_file_compressed(filename):
        new_name = filename.rstrip('.gz')
        f_in = gzip.open(filename, 'rb')
        f_out = open(new_name, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        return new_name
    else:
        return filename


def makeSingleCarrierSSIM(filename):
    """Create a single carrier SSIM file from a multiple carrier SSIM."""
    # stub for the moment
    pass

def make_recordtwo_dict(line):
    """Create a dictionary from an SSIM record 2"""

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
