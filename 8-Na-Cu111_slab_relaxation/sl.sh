#!/bin/bash
# eliminate forces of fixed atoms
fix=$1
if test -z $1; then
fix=0
fi
# get force form OUTCAR
awk -v fix="$fix" '/POSITION/,/drift/{
if($1~/^[0-9.]+$/&&$3>=fix) print $1,$2,$3,sqrt($4*$4+$5*$5+$6*$6i);
else if($1=="total") print $0
}' OUTCAR >temp.f
awk '{
if($1=="total") {print ++i,a;a=0}
else {if(a<$4) a=$4}
}' temp.f >force.conv
#sed -i '1,9d' force.conv
#rm temp.f
tail -30 force.conv >temp.f
