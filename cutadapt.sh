#!/bin/bash


outlocation=$(mktemp -d /home/galaxy/galaxy/database/XXXXXX)
SCRIPTDIR=$(dirname "$(readlink -f "$0")")

if [ $3 == "forward_mode" ]
then
    python $SCRIPTDIR"/cutadapt_wrapper.py" -i $1 -t $2 -ts $3 -fp $4 -e $5 -l $6 -of $outlocation -un $7 -O $8
    mv $outlocation"/output/trimmed.zip" $9
    cp $outlocation"/adminlog.log" "${10}"
    [ $7 == "yes" ] && mv $outlocation"/output/untrimmed.zip" "${11}"
    rm -rf $outlocation
fi

if [ $3 == "reverse_mode" ]
then
    python $SCRIPTDIR"/cutadapt_wrapper.py" -i $1 -t $2 -ts $3 -rp $4 -e $5 -l $6 -of $outlocation -un $7 -O $8
    mv $outlocation"/output/trimmed.zip" $9
    cp $outlocation"/adminlog.log" "${10}"
    [ $7 == "yes" ] && mv $outlocation"/output/untrimmed.zip" "${11}"
    rm -rf $outlocation
fi

if [ $3 == "both_mode" ]
then
    python $SCRIPTDIR"/cutadapt_wrapper.py" -i $1 -t $2 -ts $3 -fp $4 -rp $5 -e $6 -l $7 -of $outlocation -un $8 -O $9
    mv $outlocation"/output/trimmed.zip" "${10}"
    cp $outlocation"/adminlog.log" "${11}"
    [ $8 == "yes" ] && mv $outlocation"/output/untrimmed.zip" "${12}"
    rm -rf $outlocation
fi

if [ $3 == "both_mode_anchored" ]
then
    python $SCRIPTDIR"/cutadapt_wrapper.py" -i $1 -t $2 -ts $3 -fp $4 -rp $5 -e $6 -l $7 -of $outlocation -un $8 -O $9
    mv $outlocation"/output/trimmed.zip" "${10}"
    cp $outlocation"/adminlog.log" "${11}"
    [ $8 == "yes" ] && mv $outlocation"/output/untrimmed.zip" "${12}"
    rm -rf $outlocation
fi

if [ $3 == "both_three_optional_mode" ]
then
    python $SCRIPTDIR"/cutadapt_wrapper.py" -i $1 -t $2 -ts $3 -fp $4 -rp $5 -e $6 -l $7 -of $outlocation -un $8 -O $9
    mv $outlocation"/output/trimmed.zip" "${10}"
    cp $outlocation"/adminlog.log" "${11}"
    [ $8 == "yes" ] && mv $outlocation"/output/untrimmed.zip" "${12}"
    rm -rf $outlocation
fi
