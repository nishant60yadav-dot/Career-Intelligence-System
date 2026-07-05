"""
Direct Careers Scraper
Production Version (Optimized)
"""

import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

from src.models import Job


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

KEYWORDS = [
    "job",
    "jobs",
    "career",
    "careers",
    "position",
    "positions",
    "opening",
    "openings",
    "vacancy",
    "vacancies",
    "apply",
    "employment",
    "engineer",
    "scientist",
    "research",
    "chemist",
    "battery",
    "electrochem",
    "manufacturing",
    "technician",
    "graduate",
    "intern",
    "internship",
    "postdoc",
    "faculty",
    "professor",
    "developer",
    "specialist",
    "manager",
    "operator"
]

BAD_WORDS = [
    "privacy",
    "cookie",
    "cookies",
    "terms",
    "condition",
    "contact",
    "about",
    "news",
    "press",
    "media",
    "investor",
    "legal",
    "facebook",
    "linkedin",
    "instagram",
    "twitter",
    "youtube",
    "login",
    "signin",
    "register",
    "faq",
    "accessibility",
    "sitemap",
]

BAD_EXTENSIONS = (
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".css",
    ".js",
    ".zip",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
)


class DirectScraper:

    def scrape(self, company, country, career_url):

        jobs = []
        seen = set()

        try:

            response = requests.get(
                career_url,
                headers=HEADERS,
                timeout=20,
                allow_redirects=True,
            )

            if response.status_code != 200:
                return jobs

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):

                href = link["href"].strip()
                title = link.get_text(" ", strip=True)

                if len(title) < 3:
                    continue

                url = urljoin(response.url, href)
                url_lower = url.lower()

                if url == career_url:
                    continue

                if url_lower.endswith(BAD_EXTENSIONS):
                    continue

                if any(word in url_lower for word in BAD_WORDS):
                    continue

                text = (title + " " + href).lower()

                if not any(k in text for k in KEYWORDS):
                    continue

                if url in seen:
                    continue

                seen.add(url)

                title = re.sub(r"\s+", " ", title).strip()

                jobs.append(
                    Job(
                        company=company,
                        title=title,
                        country=country,
                        location="",
                        ats="Direct",
                        url=url,
                        description="",
                        date_found=datetime.today().strftime("%Y-%m-%d"),
                    )
                )

        except Exception:
            pass

        return jobs