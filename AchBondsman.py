#!/usr/bin/env python
## The tasker or the bondsman is the robot
## so here the comm mechanism is ACH

import ach
import subprocess


subprocess.check_process(["achd", "push", "159.203.67.159", "foo"])


c = ach.Channel('foo')
c.flush()



c.flush() ## clear old stuff out


class Data(Structure):
    _fields_ = [('LEB', c_double),
                ('RSP', c_double)]

dat = Data()
c.get( dat, wait=True, last=True )

print 'dat leb = %f' % (dat.LEB)

