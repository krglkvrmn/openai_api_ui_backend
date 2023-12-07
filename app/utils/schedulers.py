import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from app.auth.database import delete_expired_users


event_loop = asyncio.get_running_loop()

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: event_loop.create_task(delete_expired_users()), 'interval', seconds=30)
