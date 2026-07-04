"""
ATS Detection Module
"""

from urllib.parse import urlparse


class ATSDetector:
    """Detects the ATS platform from a career URL."""

    def detect(self, url: str) -> str:

        hostname = urlparse(url).netloc.lower()

        if "greenhouse" in hostname:
            return "Greenhouse"

        elif "lever" in hostname:
            return "Lever"

        elif "ashby" in hostname:
            return "Ashby"

        elif "workday" in hostname:
            return "Workday"

        else:
            return "Direct"