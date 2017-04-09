#!/bin/bash

debug=0
users=("alvin" "simon" "theodore" "piper" "prue" "phoebe" "paige")
sites=("https://www.bbc.co.uk" "https://www.bbc.com" "https://www.google.com" "https://www.cnn.com")
intIPs=(10.10.10.1 10.10.10.3 10.10.10.8 10.10.20.2 10.10.20.5 10.10.20.13)

secondOffset=2419200
sse=$(date +%s)
seed=$(($sse - $secondOffset))
endDate=$(date --iso-8601=seconds)
startDate=$(date --date=@$seed --iso-8601=seconds)

echo "ISO format, start time: $startDate"
echo "ISO format, end time:   $endDate"

if [[ -f exampleLog.log ]]
then
  rm ./exampleLog.log
fi

ctr=0

for i in $(seq $seed 1 $sse)
do
  ctr=$(($ctr + 1))
  if [[ $ctr%1000 = 0 ]]
  then
    echo "On $i"
  fi
  un=${users[$((RANDOM%7))]}
  s=${sites[$((RANDOM%4))]}
  ip=${intIPs[$((RANDOM%6))]}
  lit=$(date --date=@$i --iso-8601=seconds)
  echo "{\"timestamp\":\"$lit\",\"ip_address\":\"$ip\",\"username\":\"$un\",\"site\":\"$s\"}" >> ./exampleLog.log
done

echo "Script starting running at $endDate"
echo "Script completed writing at $(date --iso-8601=seconds)"
