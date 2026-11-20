cd "$(dirname "$0")"
../bvenv/bin/python scene_o.py -- plates towerlow street streetup skyline site fall shop bench hall ropetop ropecut platform mechA mechB > plates.log 2>&1
echo FINISHED >> plates.log
