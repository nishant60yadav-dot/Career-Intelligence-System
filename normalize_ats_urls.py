from playwright.sync_api import sync_playwright
import pandas as pd

EXCEL = "data/companies.xlsx"

ATS_LIST = [
    "Greenhouse",
    "Lever",
    "Workday",
    "Ashby",
    "iCIMS",
    "SuccessFactors",
    "Taleo",
    "SmartRecruiters"
]

PATTERNS = [
    "boards.greenhouse.io",
    "job-boards.greenhouse.io",
    "jobs.lever.co",
    "myworkdayjobs.com",
    "jobs.ashbyhq.com",
    "icims.com",
    "successfactors",
    "taleo"
]


df = pd.read_excel(EXCEL, sheet_name="Battery Job Database")

ats_df = df[df["ATS"].isin(ATS_LIST)].copy()

print(f"ATS Companies : {len(ats_df)}")

updated = 0

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    for idx, row in ats_df.iterrows():

        company = str(row["Company Name"]).strip()
        url = str(row["Official Careers URL"]).strip()

        print("\n" + "=" * 70)
        print(company)

        try:

            page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )

            final_url = page.url

            html = page.content()

            discovered = None

            # 1. Redirect URL
            for ptn in PATTERNS:
                if ptn.lower() in final_url.lower():
                    discovered = final_url
                    break

            # 2. Links on page
            if discovered is None:

                links = page.locator("a").evaluate_all(
                    """
                    els => els.map(e => e.href)
                    """
                )

                for link in links:

                    if not link:
                        continue

                    for ptn in PATTERNS:

                        if ptn.lower() in link.lower():

                            discovered = link

                            break

                    if discovered:
                        break

            # 3. HTML source

            if discovered is None:

                lower = html.lower()

                for ptn in PATTERNS:

                    pos = lower.find(ptn.lower())

                    if pos != -1:

                        start = lower.rfind("https://", 0, pos)

                        end = lower.find('"', pos)

                        if start != -1 and end != -1:

                            discovered = html[start:end]

                        break

            if discovered:

                print("FOUND :", discovered)

                df.loc[idx, "Official Careers URL"] = discovered

                updated += 1

            else:

                print("No ATS URL found.")

        except Exception as e:

            print("FAILED :", e)

    browser.close()

OUTPUT = "data/companies_normalized.xlsx"

with pd.ExcelWriter(
    OUTPUT,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Battery Job Database",
        index=False
    )

    pd.read_excel(
        EXCEL,
        sheet_name="Keywords"
    ).to_excel(
        writer,
        sheet_name="Keywords",
        index=False
    )

print("\n")
print("=" * 70)
print("Normalization Finished")
print("ATS Companies :", len(ats_df))
print("Updated :", updated)
print("Saved :", OUTPUT)