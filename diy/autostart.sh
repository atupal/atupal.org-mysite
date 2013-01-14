#!/bin/sh
sum=0
while true
do
    N=$(find -cmin 0.01)
#    if [ -z "$N" ]; then 
#        echo "STRING is empty" 
#    fi

    if [ -n "$N" ]; then 
        #sum=$sum+1
        let sum+=1
        clear
        echo -e "\e[1;31m restart wscgi \e[0m" 
        #echo $sum
        echo -e "\e[1;35m $sum \e[0m"
        #kill `pgrep uwsgi`
        #kill -9 `pgrep gi.sh`
        pkill python$
        sleep 0.3
        ./gi.sh &
        echo -e "\e[1;32m output:"
    fi
    sleep 0.3
done

