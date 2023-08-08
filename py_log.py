import logging
import os
import time
import datetime
import schedule
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setlogger():
    #logger = logging.basicConfig(filename='system.log', format='%(asctime)s %(message)s', datefmt=str(cur_time))
    logger = logging.getLogger('logme')
    #handler = RotatingFileHandler('py_schedule.log', maxBytes=2048000, backupCount=5)
    handler = TimedRotatingFileHandler('py_schedule.log', when='h', interval=0.1, backupCount=5, atTime=datetime.time(hour=7,minute=30))
    cur_time = time.time()
    rollover_time = handler.computeRollover(cur_time)
    print('next noon log rotation: {}'.format(datetime.datetime.fromtimestamp(rollover_time)))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def logme(msg):
    cur_time = time.strftime('%b %e %H:%M:%S', time.localtime())
    logger = logging.getLogger('logme')
    logger.info('%s %s' % (cur_time, msg))
    print(msg)

def main():
    setlogger()
    msg = 'logging me'
    #schedule.every(10).minutes.do(logme(msg))
    while True:
        #schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
