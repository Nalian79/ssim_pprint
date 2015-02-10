import gzip

def convert_to_text(gzfilename):
    """Uncompress the gzipped file, return the uncompressed file name.

    Read in the uncompressed file, and write out a new file, uncompressed,
    with the same name, minus .gz.

    args: gzfilename - the name of the gzipped file you want to uncompress.
    """

    print gzfilename
    new_name = gzfilename.rstrip('.gz')
    f_in = gzip.open(gzfilename, 'rb')
    f_out = open(new_name, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    return new_name
