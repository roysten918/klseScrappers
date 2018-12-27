#!/bin/bash
OPTIND=1
source /c/git/klseScrapers/scripts/groups.klse

CHARTDAYS=600
DATADIR=/z/data
GROUP=$MVP
ENDDT=`date +%Y-%m-%d`
OPT=1
STEPS=5
re='^[0-9]+$'
dateopt=0

#usage() { echo "Usage: group.sh -cds [counter(s)] [start date] [steps]" 1>&2; exit 1 }

while getopts ":c:C:d:g:o:s:D:" opt
do
 case "$opt" in
  C)
   CHARTDAYS=$OPTARG
   if ! [[ "$CHARTDAYS" =~ $re ]]
   then
    echo "$CHARTDAYS is not an integer number!"
    exit 2
   fi
   ;;
  D)
   DATADIR=$OPTARG
   if ! [ -d $DATADIR ]
   then
    echo $DATADIR is not a directory!
    exit 2
   fi
   ;;
  d)
   STARTDT=$OPTARG
   dateopt=1
   ;;
  c)
   GROUP=$OPTARG
   ;;
  o)
   OPT=$OPTARG
   ;;
  s)
   STEPS=$OPTARG
   if ! [[ "$STEPS" =~ $re ]]
   then
    echo "$STEPS is not an integer number!"
    exit 2
   fi
   ;;
  g)
   SET=$OPTARG
   #echo $(eval echo "\$$SET")
   GROUP=$(eval echo "\$$SET")
   ;;
  *)
   #usage
   echo "Usage: group.sh -cCdgoDs [counter] [Chartdays] [date] [groups] [opt=1234] [Dir] [steps]" 1>&2
   echo "  opt: 1 - Normal scanning, 2 - Signal scanning, 3 - Pattern scanning, 4 - Daily Charting only" 1>&2
   exit 1
   ;;
 esac
done
shift $((OPTIND-1))
[ "${1:-}" = "--" ] && shift
#echo "c=$GROUP, D=$DATADIR, d=$STARTDT, e=$ENDDT, s=$STEPS, leftovers: $@"

for i in $GROUP
do
 counter=`echo ${i} | tr '[:lower:]' '[:upper:]'`
 if [ ${dateopt} -eq 0 ]
 then
  STARTDT=`head -100 $DATADIR/mpv/${counter}.csv | tail -1 | awk -F , '{print $2}'`
 fi
 if ! [ $OPT -eq 4 ]
 then
  echo Profiling $counter, $STARTDT
  ./scripts/newprofiling.sh $counter "${STARTDT}:${ENDDT}:${STEPS}" $OPT $CHARTDAYS $DATADIR
 fi
 echo Daily Charting $counter, $STARTDT
 ./scripts/charting.sh $counter ${STARTDT}:${ENDDT} $OPT $DATADIR
done
