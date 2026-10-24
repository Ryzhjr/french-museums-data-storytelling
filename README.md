# French Museums: From Crisis to Recovery (2014–2024)

Individual EFREI ING2 Business Intelligence & Analytics project, built with Streamlit.

**Question:** How did the COVID-19 pandemic affect museum attendance in France, and how did attendance recover between 2021 and 2024?

[GitHub repository](https://github.com/Ryzhjr/french-museums-data-storytelling)

[Open the Streamlit app](https://french-museums-data-storytelling-htxicr2gvtb6r9ogxu8gjz.streamlit.app/)

[Storyboard: the story and chart sequence](STORYBOARD.md)

## Install and run

Tested with **Python 3.13**. From the project folder:

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then install the dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, use `.venv\Scripts\python.exe` instead of `python` in the last two commands.

Dependencies are pinned in `requirements.txt`: Streamlit 1.66.1, pandas 3.1.0 and Plotly 7.1.0. The CSV and GeoJSON are included, so no data download or API key is needed to run the app.

## Project structure

```text
app.py
sections/
    intro.py
    overview.py
    deep_dives.py
    conclusions.py
utils/
    io.py
    prep.py
    viz.py
data/
    ENTREES_ET_CATEGORIES_DE_PUBLIC.csv
    regions.geojson
README.md
requirements.txt
.gitignore
```

The folder name is lowercase `data` for Linux compatibility. The virtual environment, caches and secrets are excluded from Git.

## Dashboard

**Part 1 — Our Data Story** presents a fixed national analysis:

1. **The Big Picture:** attendance KPIs for 2019, 2020 and 2024.
2. **Attendance Evolution:** the years before Covid, the 2020 fall and the recovery.
3. **Regional Recovery:** a bar chart and map comparing the same **990 sites** in 2019 and 2024. Percentages compare recovery against each region's own baseline. Short comments explain regional differences and local closures.
4. **Paid vs Free Admissions:** a grouped bar chart for **814 sites** with complete, consistent records for every year from 2019 to 2024. The text describes the smaller gap during the crisis and its later increase.
5. **Key Findings:** a short conclusion, with only the main takeaway in a green `st.success()` box.

**Part 2 — Explore Museum Attendance** lets users select regions/territories, a year range and total, paid or free admissions. These filters update three KPIs, a line chart, a regional bar chart and a map. They do not change Part 1.

**Data Quality** and **Limitations** are separate text sections. There is no quality table or coloured limitations box.

## Cleaning and method

- Read the CSV in UTF-8, with a semicolon separator and string identifiers.
- Convert years and attendance fields to numeric values and trim museum names.
- Exclude all **4 rows** from two ambiguous site-year groups in 2021: **12,292 original rows → 12,288 analysis rows**.
- Report **3 missing total-admission values** and **19 paid/free/total mismatches**. Keep published counts without filling missing values.
- Keep recorded zeros, including when a site has closed. A missing record is not replaced by zero.
- Use available records for national yearly totals. For regional comparisons, match the same sites at both dates.
- Use a separate fixed 814-site panel for paid/free comparisons. Every record must satisfy paid plus free equals total.
- Cache data preparation with `st.cache_data`.

Across the same 990 sites, admissions increase from **63,471,160 in 2019** to **68,303,209 in 2024 (+7.61%)**. **9 of 19** regional panels remain below 2019.

## Limitations

Admissions are visits, not unique people. Reporting coverage changes between years, so national totals do not always describe the same museums. Common-site panels improve comparability but do not control for opening days, exhibitions or changes in activity.

The data is yearly, so it cannot show monthly changes or the exact effects of lockdown and reopening dates. Tourism, household budgets and regional resources are possible explanations, not causes measured by this CSV. Closure fields do not provide a reliable annual opening calendar.

## Data sources and licences

- **Museum admissions:** [Ministry of Culture dataset on data.gouv.fr](https://www.data.gouv.fr/datasets/frequentation-des-musees-de-france-1), under **Licence Ouverte / Open Licence**. [Etalab licence reference](https://github.com/etalab/licence-ouverte). [Original CSV](https://ministere-culture.s3.sbg.io.cloud.ovh.net/FREQ_MUSEES/ENTREES_ET_CATEGORIES_DE_PUBLIC.csv). The local file contains 20 columns and observations for 2014–2024. The historical Excel is not used.
- **Map boundaries:** [Contours administratifs](https://www.data.gouv.fr/datasets/contours-administratifs), regions 2024, 1000 m. [Original GeoJSON](https://object.data.gouv.fr/contours-administratifs/2024/geojson/regions-1000m.geojson). Attribution: **data.gouv.fr / IGN / © OpenStreetMap contributors**, under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/). The unchanged GeoJSON is included in `data/regions.geojson`. These licences apply to the data separately from the code.

The map includes overseas territories; zoom out and drag to view them.

Context for the regional comments comes from [Patrimostat 2025](https://www.culture.gouv.fr/content/download/378770/pdf_file/Patrimostat-2025.pdf), which describes renovation at the MuMa and the Approuague closure in 2023, and [2024 information on the Arche closure](https://lheuredelest.org/que-faire-en-vacances-a-saint-pierre-et-miquelon/), alongside the [museum's practical information](https://www.arche-musee-et-archives.net/fr/10-infos-pratiques.html). These sources provide context; their statistics are not merged into the dashboard.

## Deploy on Streamlit Community Cloud

Connect your GitHub account at [Streamlit Community Cloud](https://share.streamlit.io/) and create an app with:

- Repository: `Ryzhjr/french-museums-data-storytelling`
- Branch: `main`
- Main file: `app.py`
- Python version in Advanced settings: **3.13**

Dependencies are installed from `requirements.txt`. No secrets are required by this app. See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

Public app: [French Museums: From Crisis to Recovery](https://french-museums-data-storytelling-htxicr2gvtb6r9ogxu8gjz.streamlit.app/).
