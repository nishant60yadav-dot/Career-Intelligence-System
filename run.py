"""
Career Intelligence System (CIS)

Entry point of the application.
"""

from src.reader import ConfigReader
from src.scraper import JobScraper


def main():

    print("=" * 60)
    print("Career Intelligence System (CIS)")
    print("=" * 60)

    reader = ConfigReader()
    scraper = JobScraper()

    targets = reader.load_targets()

    total_jobs = 0

    for _, target in targets.iterrows():

        print(f"\nChecking: {target['Name']}")

        jobs = scraper.scrape(
            company=target["Name"],
            country=target["Country"],
            career_url=target["Career URL"]
        )

        print(f"Jobs Found: {len(jobs)}")

        total_jobs += len(jobs)

        for job in jobs:

            print(f"  • {job.title}")
            print(f"    {job.url}")

    print("\n" + "=" * 60)
    print(f"Total Jobs Found: {total_jobs}")
    print("=" * 60)


if __name__ == "__main__":
    main()