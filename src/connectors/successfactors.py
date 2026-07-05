"""
Production SAP SuccessFactors Connector
"""

import re
import requests
from datetime import datetime

from src.models import Job


class SuccessFactorsScraper:

    def _extract_company(self, url):

        patterns = [

            r"jobs\.sap\.com/job/.*",

            r"career\d+\.successfactors\.com",

            r"jobs\.successfactors\.com"

        ]

        for p in patterns:

            if re.search(p, url):
                return True

        return False

    def scrape(self, company, country, career_url):

        jobs = []

        if not self._extract_company(career_url):
            return jobs

        try:

            response = requests.get(

                career_url,

                timeout=30,

                headers={
                    "User-Agent": "Mozilla/5.0"
                }

            )

            if response.status_code != 200:
                return jobs

            # SuccessFactors implementations differ.
            # We'll enrich this connector once we
            # identify the JSON endpoint automatically.

        except Exception:
            pass

        return jobs