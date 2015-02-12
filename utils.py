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
