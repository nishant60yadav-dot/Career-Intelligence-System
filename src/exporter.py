"""
Production Job Exporter
"""

import os
from openpyxl import Workbook


class JobExporter:

    def save_excel(self, jobs, filename):

        wb = Workbook()
        ws = wb.active
        ws.title = "Jobs"

        ws.append([
            "Company",
            "Title",
            "Country",
            "Location",
            "ATS",
            "URL",
            "Date Found"
        ])

        for job in jobs:

            ws.append([
                job.company,
                job.title,
                job.country,
                job.location,
                job.ats,
                job.url,
                job.date_found
            ])

        wb.save(filename)

    def export(self, jobs, filename=None):

        os.makedirs("data", exist_ok=True)

        # If filename is supplied, save only that file
        if filename is not None:
            self.save_excel(jobs, filename)
            print(f"Saved {len(jobs)} jobs -> {filename}")
            return

        # Default export (backward compatible)

        self.save_excel(
            jobs,
            "data/today_jobs.xlsx"
        )

        top_jobs = sorted(
            jobs,
            key=lambda x: getattr(x, "score", 0),
            reverse=True
        )

        self.save_excel(
            top_jobs,
            "data/top_ranked_jobs.xlsx"
        )

        battery_keywords = [
            "battery",
            "electrochem",
            "electrode",
            "cell",
            "cathode",
            "anode",
            "lithium",
            "sodium",
            "zinc",
            "energy storage"
        ]

        battery_jobs = []

        for job in jobs:

            text = (job.title + " " + job.company).lower()

            if any(k in text for k in battery_keywords):
                battery_jobs.append(job)

        self.save_excel(
            battery_jobs,
            "data/battery_jobs.xlsx"
        )

        self.save_excel(
            jobs,
            "data/new_jobs.xlsx"
        )

        print("\n==============================")
        print("EXPORT SUMMARY")
        print("==============================")
        print(f"Today Jobs     : {len(jobs)}")
        print(f"Top Ranked     : {len(top_jobs)}")
        print(f"Battery Jobs   : {len(battery_jobs)}")
        print(f"New Jobs       : {len(jobs)}")
        print("==============================")