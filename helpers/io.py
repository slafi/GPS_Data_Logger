


def write_to_file(output_file, mode, text=''):
    """ Writes a text string to a file

    :param output_file: The file name/path to write to
    :param mode: The file access mode ('w', 'w+','a', etc.)
    :param text: The text to save into the file
    :returns: True if success, False if failure
    :rtype: Boolean
    """
    try:
        ## Open output text file
        fid = open(output_file,mode)

        fid.write(text)

        fid.close()
        
        return True
        
    except Exception as inst:
        #log.error("Exception: {}".format(inst))
        print(("Exception: {}".format(inst)))
        return False


