"""Scheduler for running RSS filter periodically"""
import logging
import asyncio
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

from main import RSSFilterApp

logger = logging.getLogger(__name__)
load_dotenv()


class RSSFilterScheduler:
    """Schedule RSS filter to run periodically"""
    
    def __init__(self, run_time: str = "09:00"):
        """
        Initialize scheduler
        
        Args:
            run_time: Time to run filter daily (format: HH:MM)
        """
        self.app = RSSFilterApp()
        self.run_time = run_time
        self._setup_schedule()
    
    def _setup_schedule(self):
        """Setup job schedule"""
        schedule.every().day.at(self.run_time).do(self._run_job)
        logger.info(f"Scheduled RSS filter to run daily at {self.run_time}")
    
    def _run_job(self):
        """Run the filter job"""
        logger.info(f"Running scheduled job at {datetime.now()}")
        try:
            articles = self.app.run_once(notify=False)
            logger.info(f"Job completed: {len(articles)} quality articles found")
        except Exception as e:
            logger.error(f"Job error: {e}", exc_info=True)
    
    def start(self):
        """Start the scheduler"""
        logger.info("Starting RSS Filter Scheduler")
        print(f"Scheduler running. Next run at {self.run_time}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            print("\nScheduler stopped")


def run_now():
    """Run filter immediately (for testing)"""
    app = RSSFilterApp()
    articles = app.run_once(notify=False)
    app.print_summary(articles)


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/scheduler.log'),
            logging.StreamHandler()
        ]
    )
    
    if len(sys.argv) > 1 and sys.argv[1] == "now":
        run_now()
    else:
        scheduler = RSSFilterScheduler(run_time="09:00")  # Run at 9:00 AM
        scheduler.start()
