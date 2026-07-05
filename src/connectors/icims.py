"""
Production iCIMS Connector
"""

import re
import requests
from datetime import datetime

from src.models import Job


class ICIMSScraper:

    def _is_icims(self, url):

        return "icims.com" in url.lower()

    def scrape(self, company, country, career_url):

        jobs = []

        if not self._is_icims(career_url):
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

            # iCIMS endpoints vary by organization.
            # We'll auto-discover the API in the
            # connector improvement sprint.

        except Exception:
            pass

        return jobs