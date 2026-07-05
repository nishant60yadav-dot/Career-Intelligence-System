"""
Production Greenhouse Connector
"""

import re
import requests
from datetime import datetime

from src.models import Job


class GreenhouseScraper:

    def _get_board_token(self, url):

        patterns = [
            r"boards\.greenhouse\.io/([^/?]+)",
            r"job-boards\.greenhouse\.io/([^/?]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def scrape(self, company, country, career_url):

        jobs = []

        token = self._get_board_token(career_url)

        if token is None:
            return jobs

        api = (
            f"https://boards-api.greenhouse.io/v1/boards/"
            f"{token}/jobs?content=true"
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

            for item in data.get("jobs", []):

                jobs.append(

                    Job(

                        company=company,

                        title=item.get("title", ""),

                        country=country,

                        location=item.get(
                            "location",
                            {}
                        ).get(
                            "name",
                            ""
                        ),

                        ats="Greenhouse",

                        url=item.get(
                            "absolute_url",
                            ""
                        ),

                        description=item.get(
                            "content",
                            ""
                        ),

                        date_found=datetime.today().strftime("%Y-%m-%d")

                    )

                )

        except Exception:
            pass

        return jobs