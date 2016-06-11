#!/usr/bin/env python3

import os
import sys
from tempfile import TemporaryDirectory

from logs.log import Log

with TemporaryDirectory() as dirname:

    file1 = os.path.join(dirname, "file1")
    file2 = os.path.join(dirname, "file2")
    file3 = os.path.join(dirname, "file3")
    file4 = os.path.join(dirname, "file4")
    file5 = os.path.join(dirname, "file5")    
    
    log = Log()

    log.set_file_levels([file1, file2], ['info', 'verbose', 'critical'])
    log.set_file_levels([file3], ['debug', 'critical'])
    log.set_file_levels([file4], ['debug', 'info'])
    log.set_file_levels([file5], ['verbose'])    

    assert(file1 in log.get_files())
    assert(file2 in log.get_files())
    assert(file3 in log.get_files())
    assert(file4 in log.get_files())
    assert(file5 in log.get_files())    
    assert(len([x for x in log.get_files()]) == 5)

    log.set_default_levels('critical')

    assert  'critical' in log.get_default_levels()
    assert(len([x for x in log.get_default_levels()]) == 1)

    log.log("log entry %d", 1)
    f1= [1]
    f2= [1]
    f3=[1]
    log.log("log entry %d", 2, levels=['info'])
    f4=[2]
    log.log_display("log entry %d", 3)
    f1.append(3)
    f2.append(3)
    f3.append(3)
    log.log_display("log entry %d", 4, levels=['info'])
    f4.append(4)
    log.log_critical("log entry %d", 5)
    f1.append(5)
    f2.append(5)
    f3.append(5)    
    log.log_info("log entry %d", 6)
    f4.append(6)
    log.log_verbose("log entry %d", 7)
    f1.append(7)
    f2.append(7)
    f5 = [7]
    log.log_debug("log entry %d", 8)
    f3.append(8)
    f4.append(8)    
    log.log_warn("log entry %d", 9)    
    f1.append(9)
    f2.append(9)
    f3.append(9)
    f4.append(9)
    f5.append(9)

    for f,l in [(file1,f1), (file2,f2), (file3,f3), (file4,f4), (file5,f5)]:
        with open(file1, 'rt') as fp:
            text = fp.read()
            for i in l:
                t = "log_entry %d" % i
                if t not in text:
                    print("String %r is not in file %r" %( t, f))
                assert t in text
            for i in range(1,10):
                if i not in l:
                    t = "log_entry %d" % i
                    assert t not in text                

