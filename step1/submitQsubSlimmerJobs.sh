#!/bin/bash

date

echo "SUBMITTING nominal"

python -u runQsubSlimmerJobs.py nominal

#sleep 5
#
#echo "SUBMITTING JECup"
#
#python -u runQsubSlimmerJobs.py JECup
#
#sleep 5
#
#echo "SUBMITTING JECdown"
#
#python -u runQsubSlimmerJobs.py JECdown
#
#sleep 5
#
#echo "SUBMITTING JERup"
#
#python -u runQsubSlimmerJobs.py JERup
#
#sleep 5
#
#echo "SUBMITTING JERdown"
#
#python -u runQsubSlimmerJobs.py JERdown
#
#sleep 5

echo "DONE"

date

