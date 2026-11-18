cd "$(dirname "$0")"
../bvenv/bin/python scene_d.py -- plates anthill antmacro wide field trail gems cut bank sack velvet money > plates.log 2>&1
echo FINISHED >> plates.log
