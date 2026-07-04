from dataclasses import dataclass


@dataclass
class Job:
    """
    Standard job object used throughout the Career Intelligence System.
    Every scraper MUST return List[Job].
    """

    company: str
    title: str
    location: str
    country: str
    url: str
    ats: str
    date_found: str