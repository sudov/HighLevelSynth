#!/bin/sh
lli=${LLVMINTERP-lli}
exec $lli \
    /home/student/vff6/ece5775/assignments/asg2/digitrec_v3_baseline/hls.prj/solution1/.autopilot/db/a.g.bc ${1+"$@"}
