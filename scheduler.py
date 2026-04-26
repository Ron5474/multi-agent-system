import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from agents.system_monitor import run_health_check
from agents.assignment_scout import run_scan
from agents.research_analyst import run_pending_tasks
from agents.chief_of_staff import send_morning_brief, consolidate_memory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", hour=8, minute=0)
def morning_brief():
    logger.info("Running morning brief")
    send_morning_brief()


@scheduler.scheduled_job("cron", hour=8, minute=5)
def assignment_scan():
    logger.info("Running Assignment Scout")
    run_scan()


@scheduler.scheduled_job("cron", minute="*/30")
def research_poll():
    logger.info("Research Analyst polling queue")
    run_pending_tasks()


@scheduler.scheduled_job("cron", hour=8, minute=10)
def morning_health_check():
    logger.info("Running System Monitor (morning)")
    run_health_check()


@scheduler.scheduled_job("cron", hour=20, minute=0)
def evening_health_check():
    logger.info("Running System Monitor (evening)")
    run_health_check()


@scheduler.scheduled_job("cron", hour=23, minute=0)
def nightly_consolidation():
    logger.info("Running nightly memory consolidation")
    consolidate_memory()


if __name__ == "__main__":
    logger.info("Scheduler starting")
    scheduler.start()
