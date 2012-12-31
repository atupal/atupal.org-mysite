#!/bin/sh
sum=0
while true
do
    N=$(find -cmin 0.01)
#    if [ -z "$N" ]; then 
#        echo "STRING is empty" 
#    fi

    if [ -n "$N" ]; then 
        sum=$sum+1
        clear
        echo "restart wscgi" 
        echo $sum
        kill `pgrep uwsgi`
        sleep 0.3
        ./gi &
    fi
    sleep 0.3
done


