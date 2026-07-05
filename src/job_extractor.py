"""
Production Job Extractor
"""

import re


class JobExtractor:

    JOB_WORDS = [

        "engineer",
        "scientist",
        "research",
        "researcher",
        "battery",
        "electrochem",
        "electrochemist",
        "chemist",
        "materials",
        "material",
        "cell",
        "developer",
        "manager",
        "specialist",
        "associate",
        "intern",
        "internship",
        "graduate",
        "phd",
        "postdoc",
        "postdoctoral",
        "technician",
        "faculty",
        "professor",
        "lecturer",
        "fellow",
        "operator",
        "manufacturing",
        "production",
        "quality",
        "r&d",
        "process",
        "electrical",
        "mechanical",
        "chemical",
        "automation",
        "controls"

    ]

    BLACKLIST = [

        "about",
        "privacy",
        "cookie",
        "cookies",
        "contact",
        "news",
        "blog",
        "events",
        "media",
        "department",
        "library",
        "admission",
        "student",
        "students",
        "campus",
        "home",
        "policy",
        "terms",
        "faq",
        "press",
        "legal",
        "accessibility",
        "sitemap",
        "investor",
        "facebook",
        "linkedin.com",
        "instagram",
        "twitter",
        "youtube",
        "login",
        "signin",
        "register"

    ]

    URL_HINTS = [

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
        "apply"

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
        ".pptx"

    )

    def is_probable_job(self, job):

        title = job.title.lower().strip()
        url = job.url.lower().strip()

        text = f"{title} {url}"

        if url.endswith(self.BAD_EXTENSIONS):
            return False

        if len(title) < 3:
            return False

        for word in self.BLACKLIST:

            if word in text:
                return False

        if any(word in title for word in self.JOB_WORDS):
            return True

        if any(word in url for word in self.URL_HINTS):
            return True

        if any(word in url for word in self.JOB_WORDS):
            return True

        return False

    def clean_jobs(self, jobs):

        cleaned = []
        seen = set()

        for job in jobs:

            if not self.is_probable_job(job):
                continue

            key = (

                job.company.lower().strip(),

                re.sub(r"\s+", " ", job.title.lower().strip()),

                job.url.lower().strip()

            )

            if key in seen:
                continue

            seen.add(key)

            cleaned.append(job)

        return cleaned