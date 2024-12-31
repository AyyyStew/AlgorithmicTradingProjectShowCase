import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime


scheduler = AsyncIOScheduler()


async def start(job_func: callable, crontab: str):
    scheduler.add_job(job_func, CronTrigger.from_crontab(crontab))
    scheduler.start()
    print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))

    # still trying to understand what magic this accomplishes
    while True:
        await asyncio.sleep(1000)
