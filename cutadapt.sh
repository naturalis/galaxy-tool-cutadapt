#!/bin/bash
if [ "$3" == "command_line" ]
then
    cutadapt_wrapper.py -i $1 -t $2 -advanced $3 -command_line "${4}" -o $5 -e -fp -rp -l -ol $6
else
    cutadapt_wrapper.py -i $1 -t $2 -e $4 -fp $5 -rp $6 -l $7 -o $8 -advanced -command_line -ol $9
fi


