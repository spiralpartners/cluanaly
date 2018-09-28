#!/bin\sh

# ../20180803_all_log_anonymous 以下にある bash_history を id time cmd の1行にするスクリプト

files=`ls ../20180803_all_log_anonymous/*/team*`

for f in $files
do
	echo $f
	history_file_name=`basename $f`
	uname=`echo $history_file_name | cut -f 1 -d '.'`
	cat $f | tr '\n' '\t' | sed -e 's/\t#/\n/g' | sed -e 's/\t$/\n/' | sed -e 's/#//' | sed -e "s/^/$uname\t/" > $history_file_name
done
