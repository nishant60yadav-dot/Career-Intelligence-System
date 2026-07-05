import requests
from openpyxl import load_workbook
from urllib.parse import urlparse

# ==========================
# SETTINGS
# ==========================

EXCEL_FILE = "battery_industry_job_database.xlsx"

# ==========================
# LOAD EXCEL
# ==========================

wb = load_workbook(EXCEL_FILE)
ws = wb.active

# Find column numbers automatically
headers = {}

for col in range(1, ws.max_column + 1):
    headers[ws.cell(row=1, column=col).value] = col

career_col = headers["Official Careers URL"]
ats_col = headers["ATS"]

# Add Status column if missing
if "Status" not in headers:
    status_col = ws.max_column + 1
    ws.cell(row=1, column=status_col).value = "Status"
else:
    status_col = headers["Status"]

# ==========================
# ATS DETECTOR
# ==========================

def detect_ats(url):

    url = url.lower()

    if "greenhouse" in url:
        return "Greenhouse"

    if "lever.co" in url:
        return "Lever"

    if "ashbyhq" in url:
        return "Ashby"

    if "workday" in url:
        return "Workday"

    if "smartrecruiters" in url:
        return "SmartRecruiters"

    if "myworkdayjobs" in url:
        return "Workday"

    if "icims" in url:
        return "iCIMS"

    if "successfactors" in url:
        return "SuccessFactors"

    if "oracle" in url or "taleo" in url:
        return "Oracle Taleo"

    return "Direct"

# ==========================
# VALIDATE LINKS
# ==========================

headers_http = {
    "User-Agent": "Mozilla/5.0"
}

for row in range(2, ws.max_row + 1):

    url = ws.cell(row=row, column=career_col).value

    if not url:
        ws.cell(row=row, column=status_col).value = "Missing URL"
        continue

    print(url)

    try:

        response = requests.get(
            url,
            timeout=15,
            headers=headers_http,
            allow_redirects=True
        )

        final_url = response.url

        ws.cell(row=row, column=career_col).value = final_url
        ws.cell(row=row, column=ats_col).value = detect_ats(final_url)

        if response.status_code == 200:
            ws.cell(row=row, column=status_col).value = "OK"
        else:
            ws.cell(row=row, column=status_col).value = f"HTTP {response.status_code}"

    except Exception as e:

        ws.cell(row=row, column=status_col).value = "FAILED"

# ==========================
# SAVE
# ==========================

wb.save(EXCEL_FILE)

print("\nDone.")