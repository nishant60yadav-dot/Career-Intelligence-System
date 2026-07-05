"""
Career Intelligence System
(Multi-threaded)
"""

TEST_MODE = None
# TEST_MODE = "Greenhouse"
# TEST_MODE = "Lever"
# TEST_MODE = "Workday"
# TEST_MODE = "Ashby"
# TEST_MODE = "SmartRecruiters"
# TEST_MODE = "iCIMS"
# TEST_MODE = "Taleo"
# TEST_MODE = "SuccessFactors"
# TEST_MODE = "Direct"

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.reader import ConfigReader
from src.scraper import JobScraper
from src.database import JobDatabase
from src.job_extractor import JobExtractor
from src.ranker import JobRanker
from src.exporter import JobExporter


MAX_WORKERS = 10


def process_company(scraper, row):

    company = row["Company Name"]
    country = row["Country"]
    career_url = row["Official Careers URL"]

    ats = row["ATS"]

    if ats is None or str(ats).strip() == "":
        ats = scraper.detector.detect(career_url)

    if TEST_MODE is not None and ats != TEST_MODE:
        return ats, []

    try:

        jobs = scraper.scrape(
            company=company,
            country=country,
            career_url=career_url,
            ats=ats
        )

        print(f"✓ {company:<35} {len(jobs):>4} jobs")

        return ats, jobs

    except Exception as e:

        print(f"✗ {company:<35} {str(e)}")

        return ats, []


def main():

    reader = ConfigReader()
    scraper = JobScraper()
    extractor = JobExtractor()
    database = JobDatabase()
    ranker = JobRanker()
    exporter = JobExporter()

    companies = reader.load_targets()

    ats_counter = Counter()
    raw_jobs = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = []

        for _, row in companies.iterrows():

            ats = row["ATS"]

            if ats is None or str(ats).strip() == "":
                ats = scraper.detector.detect(row["Official Careers URL"])

            ats_counter[ats] += 1

            futures.append(
                executor.submit(process_company, scraper, row)
            )

        for future in as_completed(futures):

            ats, jobs = future.result()

            raw_jobs.extend(jobs)

    print("\n")
    print("=" * 60)
    print("ATS SUMMARY")
    print("=" * 60)

    for ats, count in sorted(ats_counter.items()):

        print(f"{ats:<20} {count}")

    print("=" * 60)

    print(f"Raw Links      : {len(raw_jobs)}")

    clean_jobs = extractor.clean_jobs(raw_jobs)

    print(f"Probable Jobs  : {len(clean_jobs)}")

    database.update_database(clean_jobs)

    exporter.export(
        raw_jobs,
        filename="data/jobs_raw.xlsx"
    )

    exporter.export(
        clean_jobs,
        filename="data/jobs_clean.xlsx"
    )

    ranker.rank_jobs()

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()