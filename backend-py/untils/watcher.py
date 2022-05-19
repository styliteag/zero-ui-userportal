import os, sys
sys.path.append(os.getcwd())

from services.user_managment import USER_MANAGMENT
from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
    

scheduler.add_job(func=USER_MANAGMENT().watcher, trigger="interval", seconds=60)
scheduler.start()

