#!/usr/bin/env python
## The tasker or the bondsman is the robot
## so here the comm mechanism is ACH

import ach
import subprocess
from ctypes import *



subprocess.call(["achd push 159.203.67.159 foo159 &"])
subprocess.call(["achd push 44.55.143.47 foo47 &"])
print 'connected to the server'

c = []
c.append(ach.Channel('foo159'))
c.append(ach.Channel('foo47'))
c[0].flush()
c[1].flush()


class Data(Structure):
    _fields_ = [('LEB', c_double),
                ('RSP', c_double)]

dat = Data()
dat.LEB = 3.4
dat.RSP = 2.34

for chan in c:
    chan.put(dat)

for chan in c:
    rec = Data()
    chan.get(rec, wait=True, last=True)
    print 'rec leb = %f' % (rec.LEB)

for chan in c:
    chan.close()

print 'Finished'

