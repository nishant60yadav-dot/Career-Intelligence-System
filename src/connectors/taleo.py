"""
Oracle Taleo Connector
"""

import requests

from src.models import Job


class TaleoScraper:

    def scrape(self, company, country, career_url):

        jobs = []

        try:

            requests.get(
                career_url,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

        except Exception:
            pass

        return jobs