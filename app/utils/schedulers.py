import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from app.auth.database import delete_expired_guests, delete_expired_unverified_users

event_loop = asyncio.get_event_loop()

guests_deleter_scheduler = BackgroundScheduler()
guests_deleter_scheduler.add_job(lambda: event_loop.create_task(delete_expired_guests()), 'interval', seconds=30)


unverified_deleter_scheduler = BackgroundScheduler()
unverified_deleter_scheduler.add_job(
    lambda: event_loop.create_task(delete_expired_unverified_users()), 'interval', seconds=60
)
