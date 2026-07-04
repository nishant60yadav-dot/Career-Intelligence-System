"""
Greenhouse ATS scraper.
"""

from typing import List

import requests
from bs4 import BeautifulSoup

from src.models import Job


class GreenhouseScraper:

    def scrape(
        self,
        company: str,
        country: str,
        career_url: str
    ) -> List[Job]:

        response = requests.get(career_url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        jobs: List[Job] = []

        for job in soup.select("div.opening"):

            title = job.select_one("a")

            if title is None:
                continue

            url = title["href"]

            if url.startswith("/"):
                url = "https://boards.greenhouse.io" + url

            jobs.append(
                Job(
                    company=company,
                    title=title.get_text(strip=True),
                    location="",
                    country=country,
                    url=url,
                    ats="Greenhouse",
                    date_found=""
                )
            )

        return jobs