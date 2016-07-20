#!/usr/bin/env python

import ach
from ctypes import *
c = ach.Channel('foo')
c.chmod(0666) ## set so the robot can connect
c.flush() ## clear old stuff out


class Data(Structure):
    _fields_ = [('LEB', c_double),
                ('RSP', c_double)]

dat = Data()
dat.LEB = 3.4
dat.RSP = 2.34
print 'dat leb = %f' % (dat.LEB)

c.put(dat)
