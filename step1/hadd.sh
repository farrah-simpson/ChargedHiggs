#!/bin/bash

echo "HADDING NOMINAL"

python -u haddoutput.py nominal

echo "HADDING JECUP"

python -u haddoutput.py JECup

echo "HADDING JECDOWN"
python -u haddoutput.py JECdown

echo "HADDING JERUP"

python -u haddoutput.py JERup

echo "HADDING JERDOWN"

python -u haddoutput.py JERdown

echo "DONE"
