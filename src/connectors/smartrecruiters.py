"""
Production SmartRecruiters Connector
"""

import re
import requests
from datetime import datetime

from src.models import Job


class SmartRecruitersScraper:

    def _get_company(self, url):

        patterns = [
            r"careers\.smartrecruiters\.com/([^/?]+)",
            r"jobs\.smartrecruiters\.com/([^/?]+)"
        ]

        for pattern in patterns:

            m = re.search(pattern, url)

            if m:
                return m.group(1)

        return None

    def scrape(self, company, country, career_url):

        jobs = []

        company_slug = self._get_company(career_url)

        if company_slug is None:
            return jobs

        api = (
            "https://api.smartrecruiters.com/v1/companies/"
            f"{company_slug}/postings"
        )

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

            data = response.json()

            for post in data.get("content", []):

                jobs.append(

                    Job(

                        company=company,

                        title=post.get("name", ""),

                        country=country,

                        location=post.get(
                            "location",
                            {}
                        ).get(
                            "city",
                            ""
                        ),

                        ats="SmartRecruiters",

                        url=post.get(
                            "ref",
                            ""
                        ),

                        description=post.get(
                            "jobAd",
                            ""
                        ),

                        date_found=datetime.today().strftime("%Y-%m-%d")

                    )

                )

        except Exception:
            pass

        return jobs