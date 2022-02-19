# scripts-GW
Scripts developed for use at Gainwell Technologies

lookupMissingICN.sh is a shell script to identify from a list (separated by newline) internal control numbers (ICN) that are only output on the list once. The list comprises of the ICN being searched for, and the ICN returned by a query. ICN listed once were not returned by the query, and thus are missing.

watchdir.sh is a shell script to watch a directory (input argument) for changes to the files. The script updates two lists, the existing list and a new list that is created every 60 minutes to compare to the last list. Any new files are output to STDOUT (files that are not new are not output)

getIndentedClm.py takes an XML claim file that is unformatted, performs xmllint to format the file, and then searches for a unique identifier on the file using a supplementary perl script. The script outputs a formatted file with only the xml node that contains the unique identifier.
