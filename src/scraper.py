"""
Main scraper dispatcher.
"""

from typing import List

from src.ats_detector import ATSDetector
from src.greenhouse import GreenhouseScraper
from src.models import Job


class JobScraper:

    def __init__(self):

        self.detector = ATSDetector()
        self.greenhouse = GreenhouseScraper()

    def scrape(
        self,
        company: str,
        country: str,
        career_url: str
    ) -> List[Job]:

        ats = self.detector.detect(career_url)

        if ats == "Greenhouse":
            return self.greenhouse.scrape(
                company,
                country,
                career_url
            )

        return []