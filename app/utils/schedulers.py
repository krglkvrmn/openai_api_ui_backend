import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.auth.database import delete_expired_guests, delete_expired_unverified_users


guests_deleter_scheduler = AsyncIOScheduler()
guests_deleter_scheduler.add_job(delete_expired_guests, 'interval', seconds=30)


unverified_deleter_scheduler = AsyncIOScheduler()
unverified_deleter_scheduler.add_job(delete_expired_unverified_users, 'interval', seconds=60)
