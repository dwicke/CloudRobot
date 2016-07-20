#!/usr/bin/env python
## The tasker or the bondsman is the robot
## so here the comm mechanism is ACH

import ach
import subprocess
from ctypes import *



subprocess.call(["achd", "push", "159.203.67.159", "foo1", "&"])
print 'connected to the server'

c = ach.Channel('foo1')
c.flush()



c.flush() ## clear old stuff out


class Data(Structure):
    _fields_ = [('LEB', c_double),
                ('RSP', c_double)]

dat = Data()

dat.LEB = 3.4
dat.RSP = 2.34
c.put(dat)
c.close()

print 'dat leb = %f' % (dat.LEB)

