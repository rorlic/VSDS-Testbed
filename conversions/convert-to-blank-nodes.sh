#!/bin/bash
# You can call the script with 2 arguments: the folder containing the turtle files and the output folder, e.g.
# ./convert-to-blank-nodes.sh ./my_turtle_files ./my_converted_turtle_files
in=$1
out=$2
mkdir -p $out

files="$in/*.ttl"
for file in $files
do
    name=$(basename $file)
    encoding=$(file --mime-encoding $file | grep -e "[^ ]*$" -o)
    cat $file | iconv -f $encoding -t utf-8 | python3 ./as-blank-nodes.py -t "https://kbopub.economie.fgov.be/kbo#Enterprise" > $out/$name
done
