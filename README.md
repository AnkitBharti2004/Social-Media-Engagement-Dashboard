# Social Media Engagement Dashboard

A ready-to-run Streamlit project for analyzing social media content performance. It includes sample data, interactive charts, filters, content-type comparisons, best-posting-hour analysis, and CSV export.

## Features
- KPI cards: posts, engagements, impressions, engagement rate, followers gained
- Filters by platform, content type, and date range
- Engagement trends over time
- Platform comparison for likes, comments, and shares
- Content type performance and click-through rate (CTR)
- Best observed posting hour based on the selected sample
- Download filtered results as CSV
- Architecture diagram: `architecture.jpg`

## Requirements
- Python 3.10 or newer
- Internet connection for installing packages

## Run on Windows (PowerShell)
1. Extract the ZIP file.
2. Open PowerShell in the `social_media_engagement_dashboard` folder.
3. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
4. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start the dashboard:
   ```powershell
   python -m streamlit run app.py
   ```
7. Open the local URL Streamlit prints (usually `http://localhost:8501`).

## Data format
Replace `data/sample_engagement_data.csv` with data collected through authorized platform APIs. Keep these columns:
`post_id,date,platform,content_type,hour,likes,comments,shares,impressions,reach,clicks,followers_gained`

`hour` uses 24-hour local time (0–23). Use actual impression/reach values when the platform/API provides them; availability differs by platform and account type.

## Real platform integration
This starter project deliberately uses synthetic demo data and does not scrape accounts or call APIs. For production use:
- YouTube: use the official YouTube Data API for available public video statistics; access to some analytics requires OAuth and channel authorization.
- Instagram: use Meta's official Instagram Graph API for eligible professional accounts and authorized permissions.
- Store API credentials in environment variables or Streamlit secrets. Never commit tokens or passwords to GitHub.
- Respect platform terms, privacy requirements, rate limits, and the permissions granted to your account.

## Power BI / Tableau
Use the dashboard's **Download filtered CSV** button or import `data/sample_engagement_data.csv` directly into Power BI or Tableau. Suggested visuals: KPI cards, daily engagement line chart, platform comparison bar chart, content type engagement-rate chart, and hour-of-day chart.

## Important
The included data is synthetic and intended for demonstration/testing. Best posting time is only a hypothesis from the selected sample; validate it with real account data over multiple weeks.
