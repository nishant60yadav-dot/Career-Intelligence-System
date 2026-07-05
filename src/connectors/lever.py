"""
Production Lever Connector
"""

import re
import requests
from datetime import datetime

from src.models import Job


class LeverScraper:

    def _get_company(self, url):

        patterns = [
            r"jobs\.lever\.co/([^/?]+)",
            r"lever\.co/([^/?]+)"
        ]

        for pattern in patterns:

            m = re.search(pattern, url)

            if m:
                return m.group(1)

        return None

    def scrape(self, company, country, career_url):

        jobs = []

        company_name = self._get_company(career_url)

        if company_name is None:
            return jobs

        api = f"https://api.lever.co/v0/postings/{company_name}?mode=json"

        try:

            response = requests.get(
                api,
                timeout=30,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                return jobs

            postings = response.json()

            for post in postings:

                categories = post.get("categories", {})

                jobs.append(

                    Job(

                        company=company,

                        title=post.get("text", ""),

                        country=country,

                        location=categories.get(
                            "location",
                            ""
                        ),

                        ats="Lever",

                        url=post.get(
                            "hostedUrl",
                            ""
                        ),

                        description=post.get(
                            "descriptionPlain",
                            ""
                        ),

                        date_found=datetime.today().strftime("%Y-%m-%d")

                    )

                )

        except Exception:
            pass

        return jobs