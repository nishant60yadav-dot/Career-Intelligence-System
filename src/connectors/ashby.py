"""
Production Ashby Connector
"""

import re
import requests
from datetime import datetime

from src.models import Job


class AshbyScraper:

    def _get_company_slug(self, url):

        patterns = [
            r"jobs\.ashbyhq\.com/([^/?]+)",
            r"ashbyhq\.com/([^/?]+)"
        ]

        for pattern in patterns:

            m = re.search(pattern, url)

            if m:
                return m.group(1)

        return None

    def scrape(self, company, country, career_url):

        jobs = []

        slug = self._get_company_slug(career_url)

        if slug is None:
            return jobs

        api = f"https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"

        payload = {
            "variables": {
                "organizationHostedJobsPageName": slug
            },
            "query": """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoardWithTeams(
    organizationHostedJobsPageName: $organizationHostedJobsPageName
  ) {
    teams {
      jobs {
        title
        locationName
        employmentType
        secondaryLocations {
          locationName
        }
        applyUrl
        descriptionHtml
      }
    }
  }
}
"""
        }

        try:

            response = requests.post(
                api,
                json=payload,
                timeout=30,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                return jobs

            data = response.json()

            board = data.get("data", {}).get("jobBoardWithTeams", {})

            teams = board.get("teams", [])

            for team in teams:

                for post in team.get("jobs", []):

                    jobs.append(

                        Job(

                            company=company,

                            title=post.get("title", ""),

                            country=country,

                            location=post.get("locationName", ""),

                            ats="Ashby",

                            url=post.get("applyUrl", ""),

                            description=post.get(
                                "descriptionHtml",
                                ""
                            ),

                            date_found=datetime.today().strftime("%Y-%m-%d")

                        )

                    )

        except Exception:
            pass

        return jobs