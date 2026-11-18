cd "$(dirname "$0")"
../bvenv/bin/python scene_w.py -- plates sky skyempty apron front wing tail body engine top room > plates.log 2>&1
echo FINISHED >> plates.log
