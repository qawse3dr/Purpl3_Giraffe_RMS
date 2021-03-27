import logging
import libpurpl3.preferences as pref 


def confirmValidCommads(fileName: str, blackListedCommands: list) -> pref.Error:
    '''
    This function is too check a given file for blacklisted commands as defined
    by the admin of the server
    @param str fileName, the name of the script NOT INCLUDING DIRECTORY
    @param dict blackListedCommands, a dictonary of blacklisted commands, all elements of dict will be treated as a string
    @return error code of error
    '''
    try:
        script = open(fileName, "r")
        data = script.readlines()
    except IOError:
        return pref.getError(pref.ERROR_FILE_NOT_FOUND, args=(fileName))
    
    for commands in blackListedCommands:
        for lines in data:
            if commands in lines:
                #return if blacklisted command is contained within script
                return pref.getError(pref.ERROR_BLACKLISTED_COMMAND, args=(commands))
    #return if no blacklisted commands are found
    return pref.Success