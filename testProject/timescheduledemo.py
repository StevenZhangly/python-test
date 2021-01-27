from datetime import datetime
from threading import Timer


# 使用Timer
def printTimeByTimer(inc):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    t = Timer(inc, printTimeByTimer, (inc,))
    t.start()


# printTimeByTimer(5)

import sched
import time

# 生成调度器
schedule = sched.scheduler(time.time, time.sleep)


# 使用sched调度
def printTimeBySched(inc):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    schedule.enter(inc, 0, printTimeBySched, (inc,))


def main(inc=60):
    schedule.enter(0, 0, printTimeBySched, (inc,))
    schedule.run()


# main(5)


from apscheduler.schedulers.sync import SyncScheduler


def job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))


scheduler = SyncScheduler()
scheduler.add_schedule(job, 'interval', seconds=5, args=['job1']);
scheduler.start()
