if [ $# -lt 1 ]
then
 echo "group.sh <1|2> where 1=actual, 2=pattern scanning, others=daily charting only"
 exit 1
fi

HOLDINGS="ASTINO DUFU GKENT MUDA N2N NOTION PADINI PETRONM"
WATCHLIST="AEMULUS BONIA ECS HAIO HENGYUAN KGB LAYHONG MBSB MKH MMODE PADINI PETRONM SAMCHEM SCGM GCB"
MOMENTUM="BCMALL CHINWEL DANCO FLBHD KOBAY ORIENT YSPSAH"
DIVIDEND="FPI LCTITAN MAGNI UCHITEC KMLOONG MPI DUFU TONGHER CSCSTEL LIHEN TGUAN CHOOBEE GADANG OKA POHUAT PECCA SURIA"
GENISTA="APEX BURSA CBIP CIMB HIBISCS IOICORP IOIPG IVORY KPS PCHEM PRESBHD RSENA"
CONSUMER="BONIA PADINI HAIO ZHULIAN"
FURNITURE="FLBHD HEVEA"
PRECISION="DUFU KOBAY NOTION"
PAYMT="GHLSYS MPAY REVENUE"
SEMICON="KESM VITROX INARI MPI UNISEM AEMULUS"
GLOVE="TOPGLOV HARTA KOSSAN SUPERMX COMFORT"
PAPER="MUDA ORNA"
SNIPER="UCREST YONGTAI NGGB LIONIND ANNJOO KESM"
MVP="DUFU PADINI PETRONM KLSE MAGNI KAWAN"

TEST=$MVP
STARTDT="2011-05-02"
ENDDT="2018-12-14"
OPT=$1

for i in $TEST
do
 echo Profiling $i
 ./scripts/newprofiling.sh $i ${STARTDT}:${ENDDT}:2 $OPT
 echo Daily Charting $i
 ./scripts/charting.sh $i ${STARTDT}:${ENDDT}
done
