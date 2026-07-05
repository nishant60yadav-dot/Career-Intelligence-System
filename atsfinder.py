"""
ATS Finder
Reads companies.xlsx
Visits every career page
Detects ATS
Updates Excel
"""

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}


class ATSFinder:

    def detect(self, url):

        if pd.isna(url):
            return "Direct"

        url = str(url)

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20,
                allow_redirects=True
            )

            final_url = response.url.lower()

            html = response.text.lower()

            soup = BeautifulSoup(html, "html.parser")

        except Exception:

            return "Unknown"

        # --------------------------
        # URL based detection
        # --------------------------

        if "greenhouse" in final_url:
            return "Greenhouse"

        if "lever.co" in final_url:
            return "Lever"

        if "ashbyhq" in final_url:
            return "Ashby"

        if "myworkdayjobs" in final_url:
            return "Workday"

        if "myworkdaysite" in final_url:
            return "Workday"

        if "smartrecruiters" in final_url:
            return "SmartRecruiters"

        if "successfactors" in final_url:
            return "SuccessFactors"

        if "icims" in final_url:
            return "iCIMS"

        if "taleo" in final_url:
            return "Taleo"

        # --------------------------
        # HTML detection
        # --------------------------

        text = html

        if "greenhouse.io" in text:
            return "Greenhouse"

        if "boards.greenhouse.io" in text:
            return "Greenhouse"

        if "lever.co" in text:
            return "Lever"

        if "ashbyhq" in text:
            return "Ashby"

        if "myworkdayjobs" in text:
            return "Workday"

        if "wd5.myworkdayjobs" in text:
            return "Workday"

        if "smartrecruiters" in text:
            return "SmartRecruiters"

        if "successfactors" in text:
            return "SuccessFactors"

        if "icims" in text:
            return "iCIMS"

        if "taleo" in text:
            return "Taleo"

        # --------------------------
        # Script detection
        # --------------------------

        for script in soup.find_all("script"):

            s = str(script).lower()

            if "greenhouse" in s:
                return "Greenhouse"

            if "lever" in s:
                return "Lever"

            if "workday" in s:
                return "Workday"

            if "ashby" in s:
                return "Ashby"

            if "smartrecruiters" in s:
                return "SmartRecruiters"

            if "successfactors" in s:
                return "SuccessFactors"

            if "icims" in s:
                return "iCIMS"

            if "taleo" in s:
                return "Taleo"

        return "Direct"


def main():

    excel = "data/companies.xlsx"

    df = pd.read_excel(excel)

    finder = ATSFinder()

    total = len(df)

    print("=" * 70)
    print("ATS DETECTOR")
    print("=" * 70)

    for i, row in df.iterrows():

        company = row["Company Name"]

        url = row["Official Careers URL"]

        print(f"[{i+1}/{total}] {company}")

        ats = finder.detect(url)

        print("   ->", ats)

        df.loc[i, "ATS"] = ats

        time.sleep(0.5)

    df.to_excel(excel, index=False)

    print("\nFinished.")
    print("companies.xlsx updated.")


if __name__ == "__main__":
    main()