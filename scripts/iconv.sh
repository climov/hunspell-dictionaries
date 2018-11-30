#!/bin/bash
for i in `cat encodings.csv | cut -d',' -f 1`
do
    senc=`cat encodings.csv | grep "${i}" | cut -d',' -f 2`
    #echo "${i} ${senc}"
    if [ ! -f "../_hunspell/${i}/${i}.aff" ]
    then
        echo "Not found"
        exit 1
    fi
    if [ ! -f "../_hunspell/${i}/${i}.dic" ]
    then
        echo "Not found"
        exit 1
    fi
    #cp "../_hunspell/${i}/${i}.aff" "../_hunspell/${i}/${i}.aff.orig"
    #cp "../_hunspell/${i}/${i}.dic" "../_hunspell/${i}/${i}.dic.orig"
    #rm -f "../_hunspell/${i}/${i}.aff.new"
    #rm -f "../_hunspell/${i}/${i}.dic.new"
    echo "iconv -f ${senc} -t UTF-8 \"../_hunspell/${i}/${i}.aff.orig\" >\"../_hunspell/${i}/${i}.aff\" || exit 1"
    iconv -f ${senc} -t UTF-8 "../_hunspell/${i}/${i}.aff.orig" >"../_hunspell/${i}/${i}.aff" || exit 1
    echo "iconv -f ${senc} -t UTF-8 \"../_hunspell/${i}/${i}.dic.orig\" >\"../_hunspell/${i}/${i}.dic\" || exit 1"
    iconv -f ${senc} -t UTF-8 "../_hunspell/${i}/${i}.dic.orig" >"../_hunspell/${i}/${i}.dic" || exit 1
done
