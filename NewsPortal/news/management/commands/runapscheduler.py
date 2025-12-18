from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events

from news.tasks import send_weekly_digest


class Command(BaseCommand):
    help = 'Starts APScheduler'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone='UTC')
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_digest,
            trigger=CronTrigger(day_of_week='mon', hour=9, minute=0),
            id='weekly_digest',
            replace_existing=True,
        )

        register_events(scheduler)

        self.stdout.write("Scheduler started...")
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()