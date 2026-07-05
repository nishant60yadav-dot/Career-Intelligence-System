# Career Intelligence System

An AI-powered Python platform for automatically discovering, collecting, filtering, ranking, and exporting career opportunities from multiple Applicant Tracking Systems (ATS) and direct company career portals.

---

# Features

- Multi-threaded scraping
- Automatic ATS detection
- Greenhouse support
- Lever support
- Workday support
- Ashby support
- SmartRecruiters support
- iCIMS support
- Taleo support
- SuccessFactors support
- Direct careers page scraping
- Automatic job filtering
- Duplicate removal
- Daily database update
- Historical job tracking
- Battery job ranking
- Excel export
- Top jobs report
- Raw jobs report
- Clean jobs report

---

# Supported ATS

| ATS | Supported |
|------|-----------|
| Greenhouse | ✅ |
| Lever | ✅ |
| Workday | ✅ |
| Ashby | ✅ |
| SmartRecruiters | ✅ |
| iCIMS | ✅ |
| Taleo | ✅ |
| SuccessFactors | ✅ |
| Direct Websites | ✅ |

---

# Project Structure

```
Career-Intelligence-System/

│
├── data/
│   ├── companies.xlsx
│   ├── jobs_database.xlsx
│   ├── jobs_raw.xlsx
│   ├── jobs_clean.xlsx
│   └── todays_top_jobs.xlsx
│
├── src/
│   ├── connectors/
│   ├── ats_detector.py
│   ├── scraper.py
│   ├── database.py
│   ├── exporter.py
│   ├── job_extractor.py
│   ├── ranker.py
│   ├── reader.py
│   └── models.py
│
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Career-Intelligence-System.git

cd Career-Intelligence-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browser

```bash
playwright install
```

---

# Run

```bash
python run.py
```

---

# Output

The pipeline automatically generates

- jobs_raw.xlsx
- jobs_clean.xlsx
- jobs_database.xlsx
- todays_top_jobs.xlsx

---

# Workflow

```
companies.xlsx
        │
        ▼
ATS Detection
        │
        ▼
Company Scrapers
        │
        ▼
Raw Jobs
        │
        ▼
Job Extractor
        │
        ▼
Clean Jobs
        │
        ▼
Database
        │
        ▼
Ranking
        │
        ▼
Excel Reports
```

---

# Current Status

- Multi-threaded scraping implemented
- Multiple ATS supported
- Historical database implemented
- Automatic ranking implemented
- Automatic exports implemented

---

# Future Improvements

- Retry mechanism
- Logging system
- Scheduler
- Email notifications
- Web dashboard
- AI-powered semantic ranking
- Resume matching

---

# Author

**Dr. Nishant Yadav**

Assistant Professor

Materials Science • Electrochemistry • Battery Research • AI Automation

---

# License

MIT License