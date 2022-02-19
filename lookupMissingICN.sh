#!/usr/bin/bash
########################################################################
##  Usage:
##  lookupMissingICN.sh compare.txt
##
##  File ID:      lookupMissingICN.sh
##
##  Description:  This script finds missing ICN from a list containing
##                selected ICN from the iC history directory with the
##                list of ICNs that are being searched. 
##                ICN found only once are missing, as they were not 
##                returned from the reconciliation query.
##
##  Inputs:       compare.txt file is used to provide script with list
##                of ICN to identify missing claims
##
##  Outputs:      A list of missing ICN claims is output, along with the 
##                count of missing ICN.
##
########################################################################
##
##                        Modification Log
##
##  Author              Version     Date           Comments
##  Colin Weinstein     1.0         06/18/2021     Initial version
##
########################################################################

clear
sort compare.txt | uniq -u > out.txt
missingIcnCount=$(($(wc -l < out.txt)))
((N=($(wc -l < compare.txt)+$missingIcnCount)/2))
echo "There are $missingIcnCount missing ICN from $N ICN in the search."
if [ $missingIcnCount -gt 0 ]
then
  echo "Missing ICN:"
  echo "######################################################"
fi
cat out.txt
echo "######################################################"
echo "There are $missingIcnCount missing ICN from $N ICN in the search."
