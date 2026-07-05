"""
Job Model
"""

from dataclasses import dataclass


@dataclass
class Job:

    company: str
    title: str
    country: str = ""
    location: str = ""
    ats: str = ""
    url: str = ""
    description: str = ""
    date_found: str = ""