"""
Main Scraper Dispatcher
"""

from src.ats_detector import ATSDetector

from src.connectors.direct import DirectScraper
from src.connectors.greenhouse import GreenhouseScraper
from src.connectors.lever import LeverScraper
from src.connectors.workday import WorkdayScraper
from src.connectors.ashby import AshbyScraper
from src.connectors.smartrecruiters import SmartRecruitersScraper
from src.connectors.icims import ICIMSScraper
from src.connectors.taleo import TaleoScraper
from src.connectors.successfactors import SuccessFactorsScraper
from src.connectors.googlefallback import GoogleFallbackScraper


class JobScraper:

    def __init__(self):

        self.detector = ATSDetector()

        self.greenhouse = GreenhouseScraper()
        self.lever = LeverScraper()
        self.workday = WorkdayScraper()
        self.ashby = AshbyScraper()
        self.smart = SmartRecruitersScraper()
        self.icims = ICIMSScraper()
        self.taleo = TaleoScraper()
        self.success = SuccessFactorsScraper()
        self.direct = DirectScraper()
        self.google = GoogleFallbackScraper()

    def scrape(
        self,
        company,
        country,
        career_url,
        ats=None
    ):

        if not career_url:
            return []

        if ats is None or ats == "" or ats == "Unknown":

            ats = self.detector.detect(career_url)

        ats = ats.strip()

        if ats == "Greenhouse":
            return self.greenhouse.scrape(company, country, career_url)

        elif ats == "Lever":
            return self.lever.scrape(company, country, career_url)

        elif ats == "Workday":
            return self.workday.scrape(company, country, career_url)

        elif ats == "Ashby":
            return self.ashby.scrape(company, country, career_url)

        elif ats == "SmartRecruiters":
            return self.smart.scrape(company, country, career_url)

        elif ats == "iCIMS":
            return self.icims.scrape(company, country, career_url)

        elif ats == "Taleo":
            return self.taleo.scrape(company, country, career_url)

        elif ats == "SuccessFactors":
            return self.success.scrape(company, country, career_url)

        elif ats == "GoogleFallback":
            return self.google.scrape(company, country, career_url)

        return self.direct.scrape(company, country, career_url)