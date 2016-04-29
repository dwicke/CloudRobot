#!/usr/bin/env python
import ach
c = ach.Channel('foo')
c.flush()



c.flush() ## clear old stuff out


class Data(Structure):
    _fields_ = [('LEB', c_double),
                ('RSP', c_double)]

dat = Data()
c.get( dat, wait=True, last=True )

print 'dat leb = %f' % (dat.LEB)

