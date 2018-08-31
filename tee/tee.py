"""Implementing tee functionality in Python.

using pytimetee.py library.
"""
import sys

class tee(object):
    """ tee for python
    """
    def __init__(cls, _fd1, _fd2):
        cls.fd1 = _fd1
        cls.fd2 = _fd2
    def __del__(cls):
        if ((cls.fd1 != sys.stdout) and (cls.fd1 != sys.stderr)):
            cls.fd1.close()
        if ((cls.fd2 != sys.stdout) and (cls.fd2 != sys.stderr)):
            cls.fd2.close()
    def write(cls, text):
        cls.fd1.write(text)
        cls.fd2.write(text)
    def flush(cls):
        cls.fd1.flush()
        cls.fd2.flush()

    # STDOUT:
    @classmethod
    def stdout_start(cls, logfilename='stdout.log', append=True):
        cls.stdoutsav = sys.stdout
        if (append):
            cls.LOGFILE = open(logfilename, 'a')
        else:
            cls.LOGFILE = open(logfilename, 'w')
        sys.stdout = tee(cls.stdoutsav, cls.LOGFILE)
        return cls.LOGFILE
    @classmethod
    def stdout_stop(cls):
        cls.LOGFILE.close()
        sys.stdout = cls.stdoutsav

    # STDERR:
    @classmethod
    def stderr_start(cls, errfilename='stderr.log', append=True):
        cls.stderrsav = sys.stderr
        if (append):
            cls.ERRFILE = open(errfilename, 'a')
        else:
            cls.ERRFILE = open(errfilename, 'w')
        sys.stderr = tee(cls.stderrsav, cls.ERRFILE)
        return cls.ERRFILE
    @classmethod
    def stderr_stop(cls):
        cls.ERRFILE.close()
        sys.stderr = cls.stderrsav

if __name__ == '__main__' :
    print 'This prologue will appear on screen but not in a logfile'
    
    LOGFILE = tee.stdout_start(append=False) # STDOUT
    # from now on, all output is also copied to the logfile

    tee.stderr_start(append=False) # STDERR
    # from now on, all output to STDERR is also copied to tee-test.err

    print 'This text will appear on screen and also in the logfile'

    print >> sys.stderr, 'This will appear on screen and also in tee-test.err' 

    # input from keyboard does not go to logfile:
    answer = raw_input('Enter something!\n')

    # show the input to make sure it also goes into the logfile:
    print 'The user typed: %s' % (answer)

    # data written to a file is not copied to the logfile:
    DATAFILE = open('tee-test.dat','w+')
    print >> DATAFILE, range(5)
    DATAFILE.close()

    print >> LOGFILE, 'This goes to the logfile but will not appear on screen'

    tee.stdout_stop()
    # from now on, output to STDOUT will not go to tee-test.log anymore

    tee.stderr_stop()
    # from now on, output to STDERR will not go to tee-test.err anymore

    print 'This epilogue will appear on screen but not in a logfile'