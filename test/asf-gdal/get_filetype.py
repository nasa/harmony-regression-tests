import imghdr

def get_filetype(outfile):

    filetype = imghdr.what(outfile)
    return(filetype)
