#!/usr/bin/env python
#####################################################################################################
##  Usage: 
##  getFormattedClm.py --id <unique_identifier> (--x <extension>) (--p <folder path>) (--f <subdirectory name>)
##
##  File ID:      getFormattedClm.py
##  
##  Description:  Searches for file with specific extension type within the search folder.
##                Search path is hardcoded by default, or use --p / --search_path flag to 
##                specify the full path for the search.
##                Additionally, the --f / --folder flag may be used to specify a subdirectory 
##                to search from within the default search path.
## 
##  Outputs:      INDENT.<unique_identifier>
##                - file with formatted claims containing the unique identifier
## 
##  Notes:        If --folder and --search_path options are used together, the --search_path option
##                will be ignored and the --folder subdirectory will be searched instead.
## 
#####################################################################################################
##
##                        Modification Log
##
##  Author              Version     Date           Comments
##  Colin Weinstein     1.0         08/25/2021     Initial version
##  Colin Weinstein     1.1         01/17/2022     Updates to use defaul extension and delete temp file
## 
#####################################################################################################

#####################################################################################################
# Set up (Import libraries, clear terminal and set defaults for variables 
#####################################################################################################
import os
import subprocess
from optparse import OptionParser
os.system('cls' if os.name == 'nt' else 'clear')
search_path = '/export/home/dcu9126/test'
extension = '.xml'
iSuccess = 0
iFailure = 1
############################## end of set up ########################################################
#####################################################################################################


#####################################################################################################
#
# Function Name:    main()
#
# Description:      This is the main function that controls the processing. It will create an indented
#                   XML output file from the XML file found in the search path directory.
#                   The program will also create an indented XML output file containing only the claim 
#                   with the unique identifier provided as an input argument by the user.
#
# Arguments:        input - string identifier   - Unique identifier to search for to find claim
#                   input - string extension    - Filetype extension to search for (Default = '.xml')
#                   input - string search_path  - Full path to directory that is to be searched for file
#
# Return Codes:     0 - iSuccess - The function executed successfully.
#                   1 - iFailure - The function did not execute successfully.
#
# Notes:            None.
#
#####################################################################################################
def main(identifier, extension, search_path):
#####################################################################################################
# Initialize Return Code.
# Read files from search path
# Get filepath to 'getCmlXml.pl' file
# Look for file with specified extension type
# Execute xmllint on located file to write to indented output file INDENT.filename
# Execute getClmXml.pl on indented output file to retreive claim with unique identifier.
# Return iRc. 
#####################################################################################################
  iRc = iFailure
  files = readFilesFromSearchPath(search_path)
  getClmXmlFilePath = getFilepathToGetClmXml()
  if files != '' and getClmXmlFilePath != '':
    # Search path provided is valid and getClmXml.pl found in $PERLPATH
    msg = 'Looking for ' + extension + ' file in ' + search_path
    print(msg)
    filename = lookForFile(files, extension, search_path)

    if filename != '':
      # File with proper extension found in directory
      filepathname = os.path.join(search_path, filename)
      indented_xml_outputname = 'INDENT.' + filename
      indented_clm_outputname = 'INDENT.' + identifier
  
      # Runs bash xmlllint command to format original file into new file
      msg = extension + ' file ' + filename + ' found!\nFormatting file...\n'
      print(msg)
      executeXmlLint(indented_xml_outputname, filepathname)
  
    
      # Runs getClmXml.pl script to get claim from new, indented file
      msg = 'File formatted. Attempting to extract claim with unique identifier ' + identifier + ' from file...'
      print(msg)
      executeGetClmXml(indented_clm_outputname, indented_xml_outputname, identifier, getClmXmlFilePath)
  
      if os.stat(indented_clm_outputname).st_size > 0:
        os.remove(indented_xml_outputname)
        iRc = iSuccess
      else:
        os.remove(indented_clm_outputname)
        msg = 'Identifier ' + identifier + ' not found in search path ' + search_path
        print(msg)
    else:
      # Else file not found in directory
      printFileNotFoundMsg(extension, search_path)
  
#####################################################################################################
# Return code of the function
#####################################################################################################
  return iRc  
############################## end of main() function ###############################################
#####################################################################################################
  

#####################################################################################################
#
# Function Definitions 
#
#####################################################################################################
#####################################################################################################
#
# Function Name:    init()
#
# Description:      Create and use parser to fetch command argument options.
#
# Arguments:        N/A
#
# Returned Data:    output - string options.identifier  - Unique identifier to search for to find claim
#                   output - string options.extension   - Filetype extension to search for (Default = '.xml')
#                   output - string options.folder      - Subdirectory in default search directory to search
#                   output - string options.search_path - Full path to directory that is to be searched for file
#
# Notes:            If --folder and --search_path options are used together, the --folder option
#                   will be ignored and the --search_path directory will be used for the search.
#
#####################################################################################################
def init():
#####################################################################################################
# Setup parser for command line arugments
# Fetch and return data from parser
#####################################################################################################
  parser = OptionParser()
  parser.add_option('--id', '--identifier',           dest='identifier', 
                    help='input for unique identifier to find and get claim')
  parser.add_option('--x', '--ext', '--extension',    dest='extension', 
                    help='set extension of file to search for. default: .xml')
  parser.add_option('--p', '--path',                  dest='search_path', 
                    help='set full path to search in for raw claim file. does not search subdirectories.')
  parser.add_option('--f', '--folder',                dest='folder', 
                    help='set subdirectory to search from within default directory. do not include /')
  # get and set command line arugments into local variables using parser
  options, args = parser.parse_args()
#####################################################################################################
# Return variable from function
#####################################################################################################
  return options
############################## end of init() function ###############################################
#####################################################################################################


#####################################################################################################
#
# Function Name:    readFilesFromSearchPath()
#
# Description:      Input search_path directory is searched, and all files are returned as an array.
#                   If search_path is not found, '' is returned
#
# Arguments:        input - string search_path - Full path to directory that is to be searched for file
#
# Return Codes:     ['filename0', 'filename1', ...] - array containing string of all files in the search directory
#
# Notes:            None.
#
#####################################################################################################
def readFilesFromSearchPath(search_path):
#####################################################################################################
# Checks if search path is a valid directory in the system
# Return the files in the directory if valid, otherwise return '' and print and error message
#####################################################################################################
  # Verify search path exists in system
  files = ''
  if os.path.exists(search_path):
    files = os.listdir(search_path)
  else:
    printInvalidSearchPathMsg(search_path)
  return files
############################## end of readFilesFromSearchPath() function ############################
#####################################################################################################


#####################################################################################################
#
# Function Name:    lookForFile()
#
# Description:      Searches for a file with the given extension in the given search_path directory.
#
# Arguments:        input - string[] files      - Array of filenames in search directory
#                   input - string extension    - Filetype extension to search for (Default = '.xml') 
#                   input - string search_path  - Full path to directory that is to be searched for file
#
# Return Variable:  output - string filename - name of file found to be formatted
#
# Notes:            None.
#
#####################################################################################################
def lookForFile(files, extension, search_path):
#####################################################################################################
# Searches for file with specified extension in search path directory
# Ignores files with INDENT. prefix as these files are already formatted
# Returns filename if file with specified extension is found, otherwise returns ''
#####################################################################################################
  # Get file name from directory by searching for file of specified type (default: .xml)
  filename = ''
  for file in files:
    if ('INDENT.' not in file) and (extension in file): 
      filename = file
      break
#####################################################################################################
# Return variable
#####################################################################################################
  return filename  
############################## end of lookForFile() function ########################################
#####################################################################################################


#####################################################################################################
#
# Function Name:    executeXmlLint()
#
# Description:      Execute xmllint bash command on file found in search_path directory. The output of 
#                   xmllint is written to new file with filename = indented_xml_outputname
#
# Arguments:        input - string indented_xml_outputname - name of indented xml file to create and write to
#                   input - string filepathname            - filepath and name for raw xml file to format
#
# Return Codes:     0 - iSuccess - The function executed successfully.
#                   1 - iFailure - The function did not execute successfully.
#
# Notes:            None.
#
#####################################################################################################
def executeXmlLint(indented_xml_outputname, filepathname):
#####################################################################################################
# Creates file and command for indenting input file
# Calls xmllint bash command
# Print debugging output
# Return iRc
#####################################################################################################
  iRc = iFailure
  indented_xml_file = open(indented_xml_outputname, "a")
  bash_cmd = 'xmllint --format --recover ' + filepathname
  ret = subprocess.call(bash_cmd.split(), stdout=indented_xml_file)
  indented_xml_file.close()
  if ret == 0:
    iRc = iSuccess
  printXmllintRc(ret)
#####################################################################################################
# Return code
#####################################################################################################
  return iRc
############################## end of executeXmlLint() function #####################################
#####################################################################################################


#####################################################################################################
#
# Function Name:    getFilepathToGetClmXml()
#
# Description:      Attempts to search the directory located at the $PERLPATH environment variable
#                   and locate the getClmXml.pl file. The filepath to getClmXml.pl to returned as a string.
#
# Arguments:        N/A
#
# Return Variable:  string getClmXmlFilePath - filepath to getClmXml.pl
#
# Notes:            None.
#
#####################################################################################################
def getFilepathToGetClmXml():
#####################################################################################################
# Retrieves path to perl script from environment variable $PERLPATH
# If perl path directory is found in system, checks for getClmXml.pl
# Returns perlpath/getClmXml.pl if found, otherwise returns '' and prints an error message
#####################################################################################################
  # Try to get $PERLPATH environment variable to locate getClmXml.pl
  getClmXmlFilePath = ''
  try:
    perlpath = os.environ['PERLPATH']
    if os.path.exists(perlpath):
      plFiles = os.listdir(perlpath)
      for file in plFiles:
        if 'getClmXml.pl' in file:
          getClmXmlFilePath = os.path.join(perlpath, file)
          break
    if getClmXmlFilePath == '':
      printInvalidPerlPathMsg(perlpath)
  except KeyError:
    printKeyErrorExceptionMsg()
  except:
    printUnknownExceptionMsg()
#####################################################################################################
# Return variable
#####################################################################################################
  return getClmXmlFilePath
############################## end of getFilepathToGetClmXml() function #############################
#####################################################################################################


#####################################################################################################
#
# Function Name:    executeGetCmlXml()
#
# Description:      Execute getClmXml.pl script to retrieve the claim with the specified identifier
#                   from the indented xml created from the file found in the search_path directory. 
#                   The output of getClmXml.pl is written to a new file with filename = indented_clm_outputname
#                   
#
# Arguments:        input - string indented_clm_outputname - filename of new indented claim file
#                   input - string indented_xml_outputname - filename of whole indented xlm file
#                   input - string identifier              - Unique identifier to search for to find claim
#                   input - string getClmXmlFilePath       - filepath for getClmXml.pl
#
# Return Codes:     0 - iSuccess - The function executed successfully.
#                   1 - iFailure - The function did not execute successfully.
#
# Notes:            None.
#
#####################################################################################################
def executeGetClmXml(indented_clm_outputname, indented_xml_outputname, identifier, getClmXmlFilePath):
#####################################################################################################
# Creates file for intented claim output
# Creates bash script for calling getClmXml.pl
# Calls getClmXml.pl bash command
#####################################################################################################
  iRc = iFailure
  indented_clm_file = open(indented_clm_outputname, "a")
  subprocess.call([getClmXmlFilePath, indented_xml_outputname, identifier], stdout=indented_clm_file)
  indented_clm_file.close()
  if os.stat(indented_xml_outputname).st_size != 0:
    iRc = iSuccess
#####################################################################################################
# Return code
#####################################################################################################
  return iRc
############################## end of executeGetClmXml() function ###################################
#####################################################################################################


#####################################################################################################
#
# Print Functions 
#
#####################################################################################################
def printResult(return_code):
  if return_code == iSuccess:
    print('Done!')
  else:
    print('Program failed!')

def printXmllintRc(return_code):
  switcher = {
    0: 'Successfully performed xmllint on file',
    1: 'Unclassified error',
    2: 'Error in DTD',
    3: 'Validation error',
    4: 'Validation error',
    5: 'Error in schema compilation',
    6: 'Error writing output',
    7: 'Error in pattern',
    9: 'Out of memory error'
  }
  print(switcher.get(return_code, 'Unclassified error'))

def printGetClmXmlError(return_code):
  switcher = {
    0: 'Successfully performed xmllint on file',
    1: 'Unclassified error',
    2: 'Error in DTD',
    3: 'Validation error',
    4: 'Validation error',
    5: 'Error in schema compilation',
    6: 'Error writing output',
    7: 'Error in pattern',
    9: 'Out of memory error'
  }
  pass
  
def printNoIdentifierMsg():
  noIdentifierMsg = ['Error occured\n',
                     'No unique identifier included to search claim for.']
  noIdentifierMsg = ''.join(noIdentifierMsg)
  print(noIdentifierMsg)

def printFileNotFoundMsg(extension, search_path):
  fileNotFoundMsg = ['Error occured\n',
                     extension, ' file not found in ', search_path]
  fileNotFoundMsg = ''.join(fileNotFoundMsg)
  print(fileNotFoundMsg)

def printInvalidSearchPathMsg(search_path):
  invalidSearchPathMsg = ['Error occured\n',
                          'Search path ', search_path, ' for file does not exist.\n',
                          'Please verify search path.']
  invalidSearchPathMsg = ''.join(invalidSearchPathMsg)
  print(invalidSearchPathMsg)

def printInvalidPerlPathMsg(perlpath):
  invalidPerlPathMsg = ['Error occured\n',
                        'getClmXml.pl not found in ', perlpath, '. '
                        'Please verify path to getClmXml.pl file']
  invalidPerlPathMsg = ''.join(invalidPerlPathMsg)
  print(invalidPerlPathMsg)

def printKeyErrorExceptionMsg():
  keyErrorExceptionMsg = ['KeyError exception occured.\n'
                          'Please define environment variable $PERLPATH in your .profile file or hardcode directory into program\n',
                          'For example: Add line in .profile: export PERLPATH=/export/home/dcxXXXX/develop/perl']
  keyErrorExceptionMsg = ''.join(keyErrorExceptionMsg)
  print(keyErrorExceptionMsg)
 
def printUnknownExceptionMsg():
  unknownExceptionMsg = 'Unknown exception occured.'
  print(unknownExceptionMsg)
############################## end of print messages ################################################
#####################################################################################################


#####################################################################################################
# Execute only if program was called as a script, not if it was imported
#####################################################################################################
# Initialize program by getting identifier, extension and search_path
# Fetches options from init() function
# Execute main() if identifier is provided by the user
#####################################################################################################
if __name__ == '__main__':
  options = init()
  if options.identifier:
    identifier = options.identifier
  if options.extension:
    extension = options.extension
  if options.folder:
    search_path = os.path.join(search_path, options.folder)
  elif options.search_path:
    search_path = options.search_path
  
  if identifier:
    ret = main(identifier, extension, search_path)
    printResult(ret)
  else:
    printNoIdentifierMsg()
#####################################################################################################
############################## end of getIndentedClmXml.py program ##################################
#####################################################################################################
