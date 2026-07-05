"""
ATS Detector
"""


class ATSDetector:

    def detect(self, career_url):

        if not career_url:
            return "Direct"

        url = career_url.lower()

        if "greenhouse" in url:
            return "Greenhouse"

        if "lever.co" in url:
            return "Lever"

        if "ashbyhq" in url:
            return "Ashby"

        if "myworkdayjobs" in url:
            return "Workday"

        if "myworkdaysite" in url:
            return "Workday"

        if "smartrecruiters" in url:
            return "SmartRecruiters"

        if "icims" in url:
            return "iCIMS"

        if "taleo" in url:
            return "Taleo"

        if "successfactors" in url:
            return "SuccessFactors"

        return "Direct"