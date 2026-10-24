# French Museums: From Crisis to Recovery (2014–2024)

Individual EFREI ING2 Business Intelligence & Analytics project. This single-page Streamlit app studies recorded museum admissions before, during and after the COVID-19 crisis. It is intended for students and cultural decision-makers.

**Question:** How did the COVID-19 pandemic affect museum attendance in France, and how did attendance recover between 2021 and 2024? The app describes changes, without estimating a causal effect.

## Install and run locally

Tested with Python 3.13. From the project folder:

```bash
python -m venv .venv
```

Activate the environment with `.venv\Scripts\Activate.ps1` in Windows PowerShell, or `source .venv/bin/activate` on macOS/Linux. Then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run `.venv\Scripts\python.exe -m streamlit run app.py` after installing requirements with that same Python executable.

The only direct libraries are **Streamlit 1.66.1**, **pandas 3.1.0** and **Plotly 7.1.0**. Their required packages are installed automatically. The app reads local files and makes no data API or map-tile request at startup. A modern browser with WebGL support is needed for the interactive map.

## Files

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
```

The environment `.venv/` is only for local execution and is not part of the submission files.

## Source and licences

The only statistical source is the [Ministry of Culture dataset on data.gouv.fr](https://www.data.gouv.fr/datasets/frequentation-des-musees-de-france-1), under **Licence Ouverte / Open Licence** (`fr-lo`). [Licence reference from Etalab](https://github.com/etalab/licence-ouverte). The portal does not state a licence version. Keep this source attribution when reusing the data.

The portal calls the resource `frequentation-des-musees-de-france.csv`, while its [download URL](https://ministere-culture.s3.sbg.io.cloud.ovh.net/FREQ_MUSEES/ENTREES_ET_CATEGORIES_DE_PUBLIC.csv) ends in `ENTREES_ET_CATEGORIES_DE_PUBLIC.csv`. The local original matches that download by SHA-256. Resource update: **19 October 2026**; verified **24 October 2026**. The CSV has **12,292 rows**, 20 columns and observations for **2014–2024**. Empty coverage metadata on the portal do not mean the year and geographical columns are absent from the CSV. The historical Excel is not used.

The map uses [Contours administratifs](https://www.data.gouv.fr/datasets/contours-administratifs), published by **data.gouv.fr**, **Régions 2024, 1000 m**, resource updated **17 April 2025**. [Original GeoJSON](https://object.data.gouv.fr/contours-administratifs/2024/geojson/regions-1000m.geojson). Attribution: **data.gouv.fr / IGN / © OpenStreetMap contributors**. Contains information from Contours administratifs, available under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/). The unchanged database is supplied as `data/regions.geojson`, under that licence. It provides boundaries only. All 19 statistical regions/territories match a boundary; other features receive no invented statistics. These data licences are separate from the code.

The map starts over mainland France when mainland regions have a valid comparison. Overseas comparisons remain included and can be viewed by zooming out and dragging. An overseas-only comparison centres the map on its actual boundaries. No additional map selector or location dataset is used.

## Method, story and limits

The single page now has two distinct parts. **Part 1 is a fixed national Data Story**, prepared in the cached `get_data()` before any sidebar filters are applied. **Part 2 is Explore Museum Attendance**, with independent filtered tables and short factual labels. Changing the sidebar never changes Part 1.

`get_data()` retains the professor's `load_data()` then `make_tables()` pattern and `st.cache_data`. The CSV uses UTF-8, `sep=";"` and string IDs. Four ambiguous 2021 site-year records are isolated, leaving **12,288 analytical rows**. The **19 paid/free/total mismatches** are reported while published totals remain in attendance analysis. Missing counts stay missing; an entirely missing sum stays missing. No additional statistical source or new dependency is used.

### Part 1: our fixed story

1. **The Big Picture:** three fixed observed totals for 2019, 2020 and 2024, with a brief explanation of the shock and outcome.
2. **Attendance Evolution:** one annual line covering 2014-2024. Annual changes explain the earlier fluctuations, the partial 2021 return, the large 2022 rebound and the slower 2023-2024 increase. Hover gives site coverage.
3. **Regional Recovery:** the existing bars and map compare 2019 and 2024 for the same **990 sites** with known total admissions at both dates. Text distinguishes current volume, absolute change, percentage change and panel size. Illustrative admissions-per-site averages are not quality scores. The map and bars use the same percentage scale; two separate volume maps are unnecessary.
4. **Paid vs Free:** one additional grouped bar chart uses the same **814 sites** with complete, consistent paid/free/total records in every year from 2019 to 2024. Each row must satisfy paid plus free equals total. Payment shares divide by the total of these same records. This balanced payment panel differs from the regional panel and national observed totals.
5. **Key Findings:** short synthesis of observed facts, interpretations and explicitly unproven hypotheses.

The default national observed totals are **65,933,388 in 2019**, **23,819,133 in 2020** (-63.87%) and **71,192,245 in 2024** (+7.98% from 2019). The observed count first exceeds 2019 in **2023**. For the same 990 sites, the 2019/2024 increase is **7.61%**, while **9 of 19** regional panels remain below their earlier count. The analytical 2021 total is **31,011,196** after the four exclusions.

In the compatible 814-site payment panel, free admissions rise from **25,331,369** in 2019 to **26,530,126** in 2024, while paid admissions rise from **34,759,761** to **38,104,267**. The free share falls from **42.15% to 41.05%**. An increase in free volume is therefore different from an increase in its proportion. Neither this share nor this smaller panel should be calculated against the full national total.

### Part 2: user exploration

The sidebar offers only **Regions / territories**, **Year range** (default 2014-2024) and **Metric** (Total/Paid/Free). Three interactive KPIs show the last selected year's recorded count, the observed percentage change between selected endpoints and the known site count at the last date. An endpoint percentage needs different years, known values and a positive starting total.

The shared line function shows the chosen period. Shared bar/map functions compare its **first and last selected years**, using the same sites with known values at both endpoints. A zero combined starting total has no valid percentage. A single-year or empty selection gives a clear message instead of an invented change. There are no long automatic interpretations or hypotheses in the exploration section.

There are **four fixed-story charts and three default exploration charts**. They serve the two explicitly requested purposes; no extra page, selector, table or chart beyond these is added. Chart keys keep the reused functions independent. The four recommended section modules and three utility modules are retained.

### Quality and limits

The mandatory quality section gives missing attendance values, ambiguous keys, consistency checks and filtered missingness. The CSV is unchanged. Admissions are visits, not unique people. Coverage changes across years and regions; some sites may combine several museums. The portal's current collection definitions are limited. Closure fields are not a yearly opening calendar. Common-site comparisons still exclude missing records and do not control for exhibitions or opening days.

The national narrative links to official historical context: the [2015–2016 attacks and tourism](https://www.entreprises.gouv.fr/la-dge/publications/826-millions-de-touristes-etrangers-en-france-en-2016), [lockdown on 17 March 2020](https://www.interieur.gouv.fr/archive/allocution-de-christophe-castaner-ministre-de-l-interieur-a-l-issue-du-conseil-des-ministres-du-17-mars-2020), [the tourism disruption](https://blog.insee.fr/tourisme-recherchesgoogle-avisairbnb-et-statistiques/), [cultural reopening on 19 May 2021](https://www.culture.gouv.fr/actualites/Reouverture-des-lieux-culturels-un-dispositif-general-et-progressif), [easing of rules in March 2022](https://www.info.gouv.fr/actualite/covid-19-le-gouvernement-leve-le-pass-vaccinal-et-le-port-du-masque-a-compter-du-14-mars) and [the return of tourism in 2022](https://www.insee.fr/fr/information/6669676). These sources provide context only; no external statistical series is joined or plotted.

The contribution of these events to our museum counts, visitor fears, gradual adjustment and a stronger wish for cultural outings remain **hypotheses**, not effects measured by the CSV. A missing site record is not proof of a COVID-related closure. Recorded zeros remain in observed totals, but missing records are never imputed as zeros. The 2023–2024 high counts are records within this file, not claims about all-time national records or statistical significance. The app does not infer visitor identities or claim that the dataset proves a causal effect of the pandemic or a public policy. No sampling is used. The annual slider adapts the professor's example daily picker to yearly data.

## Later submission requirements

The professor also requests a report, storyboard, repository link, a validated deployed-app URL, a 2-4 minute demo and a ZIP containing code, README and dataset or link, named `StApp26_<student_number>_<surname>_BIA.zip`. The method/results and story outline above preserve the useful report and storyboard information. These submission tasks are postponed until the local app is validated. No new ZIP, repository, deployment, video or delivery script is prepared in this simplified version.
