"""
Production Workday Connector
Supports pagination.
"""

import re
import requests
from datetime import datetime

from src.models import Job


class WorkdayScraper:

    def _parse_url(self, url):

        patterns = [

            r"https://([^.]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/?]+)",

            r"https://jobs\.myworkdaysite\.com/recruiting/([^/]+)/([^/?]+)"

        ]

        for pattern in patterns:

            m = re.match(pattern, url)

            if not m:
                continue

            if "myworkdaysite" in pattern:

                return {
                    "tenant": m.group(1),
                    "server": "myworkdaysite",
                    "site": m.group(2)
                }

            return {
                "tenant": m.group(1),
                "server": m.group(2),
                "site": m.group(3)
            }

        return None

    def scrape(self, company, country, career_url):

        jobs = []

        cfg = self._parse_url(career_url)

        if cfg is None:
            return jobs

        if cfg["server"] == "myworkdaysite":

            api = (
                f"https://jobs.myworkdaysite.com/"
                f"wday/cxs/{cfg['tenant']}/{cfg['site']}/jobs"
            )

        else:

            api = (
                f"https://{cfg['tenant']}."
                f"{cfg['server']}.myworkdayjobs.com/"
                f"wday/cxs/{cfg['tenant']}/{cfg['site']}/jobs"
            )

        offset = 0
        limit = 20

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": career_url
        }

        while True:

            payload = {
                "appliedFacets": {},
                "limit": limit,
                "offset": offset,
                "searchText": ""
            }

            try:

                response = requests.post(
                    api,
                    json=payload,
                    headers=headers,
                    timeout=30
                )

                if response.status_code != 200:
                    break

                data = response.json()

                postings = data.get("jobPostings", [])

                if not postings:
                    break

                for post in postings:

                    jobs.append(

                        Job(

                            company=company,

                            title=post.get("title", ""),

                            country=country,

                            location=post.get("locationsText", ""),

                            ats="Workday",

                            url=career_url.rstrip("/") +
                            "/job/" +
                            post.get("externalPath", ""),

                            description=post.get("bulletFields", ""),

                            date_found=datetime.today().strftime("%Y-%m-%d")

                        )

                    )

                if len(postings) < limit:
                    break

                offset += limit

            except Exception:

                break

        return jobs