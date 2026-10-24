# Project Report — French Museums: From Crisis to Recovery (2014–2024)

Individual EFREI ING2 Business Intelligence & Analytics project

[Live application](https://french-museums-data-storytelling-htxicr2gvtb6r9ogxu8gjz.streamlit.app/) · [GitHub repository](https://github.com/Ryzhjr/french-museums-data-storytelling) · [Storyboard](STORYBOARD.md)

## 1. Introduction and objective

Museums connect people with art, history and culture. During the Covid crisis, closures and travel restrictions reduced opportunities to visit them. My project studies how recorded museum attendance changed before, during and after this period.

The main question is: **How did the COVID-19 pandemic affect museum attendance in France, and how did attendance recover between 2021 and 2024?**

The dashboard is for students and people interested in cultural activity. Its goal is to explain the main changes with simple charts and short comments. It describes attendance patterns; it does not measure the exact causal effect of Covid.

## 2. Dataset and sources

I used the Ministry of Culture dataset **ENTREES_ET_CATEGORIES_DE_PUBLIC.csv**, available on data.gouv.fr under the Open Licence. It contains **12,292 rows and 20 columns**, with yearly observations from **2014 to 2024**.

The main fields used are the site identifier, museum name, year, region, total admissions, paid admissions and free admissions. Admissions count visits, not unique people. Some reporting sites may represent more than one museum.

For the map, I used a separate GeoJSON with regional boundaries. It adds geographical shapes, not attendance statistics. The optional historical Excel file was not needed because the main CSV covers the project period.

## 3. Data preparation

I read the CSV using UTF-8 and a semicolon separator. UTF-8 keeps accents in museum and region names correct. I kept identifiers as strings, converted years and admission counts to numbers, and removed extra spaces around museum names.

I checked missing values, duplicate records and the relationship between paid, free and total admissions:

- There are **no exact duplicate rows**.
- Two site-year groups in 2021 contain conflicting records. I excluded all **4 rows** from these groups rather than choosing one version without a reason. This leaves **12,288 rows** for analysis.
- The original file has **3 missing total-admission values**.
- In **19 records**, paid plus free admissions does not match the published total. I kept published totals for the general attendance analysis.
- Missing values remain missing. Recorded zeros remain in the data, because zero visits can describe a real situation such as a closure.

The original CSV is unchanged. Cleaning happens in Python when the app loads.

## 4. Comparison methods

I used three different groups of records, because each comparison answers a different question.

**National trends:** the line chart and main KPIs use the available records for each year. This shows recorded activity, but the number of sites changes between years.

**Regional recovery:** I matched the same **990 sites** with known total admissions in both 2019 and 2024. This avoids comparing two different lists of sites. Percentage change is calculated as `(2024 admissions / 2019 admissions - 1) × 100`. It compares each region with its own starting level.

**Paid and free admissions:** I used a separate group of **814 sites** with complete records in every year from 2019 to 2024. For these records, paid plus free must equal total admissions. This makes the payment comparison more consistent. These totals must not be mixed with the full national totals or the 990-site regional group.

## 5. Main results

### A major fall, followed by a gradual recovery

National recorded admissions fall from **65,933,388 in 2019** to **23,819,133 in 2020**, a decrease of **63.87%**. This sharp fall matches the period of lockdowns, museum closures and travel restrictions.

Attendance starts to rise in 2021 and increases strongly in 2022, but remains below 2019. The recorded total passes the 2019 level in 2023. In 2024, it reaches **71,192,245**, or **7.98% above 2019**. This comparison uses changing yearly coverage, so the fixed-site comparison is also important.

### Overall recovery, with regional differences

Across the same 990 sites, admissions rise from **63,471,160 in 2019** to **68,303,209 in 2024**, an increase of **7.61%**. Overall, attendance has returned to a level close to before Covid, with a modest increase.

However, **9 of 19 regional groups** remain below 2019. Île-de-France records **40,719,724 admissions** in 2024, with growth of **11.05%**. Pays de la Loire records fewer admissions, **1,856,182**, but stronger growth of **22.13%**. More visits does not always mean faster percentage recovery.

Some large falls reflect local situations. The MuMa in Mayotte reports zero admissions in 2024, while published information describes a closure for renovation. The Arche in Saint-Pierre-et-Miquelon falls from **4,303 to 171 admissions**; information for 2024 reports a closure for building works. Each territory has only one site in our comparison, so one museum strongly affects its result. In Guyane, the Approuague ecomuseum closed in 2023 and reports zero admissions in the 2024 CSV.

### Paid and free admissions

In the 814-site group, both paid and free admissions fall during the crisis. Free admissions fall less compared with 2019, so the gap becomes smaller in 2020 and 2021. Both rise in 2022 and 2023. In 2024, paid admissions rise while free admissions fall.

Free admissions are still higher in 2024 than in 2019, rising from **25,331,369 to 26,530,126**. However, their share falls from **42.15% to 41.05%**. More free visits does not necessarily mean a larger share of all visits.

Tourism and household budgets could help explain the pattern. For example, fewer tourists could reduce paid visits, while lower income could make free visits more attractive after reopening. These are hypotheses: the dataset does not show visitor income, nationality or choices.

## 6. Storytelling and application design

The first part follows a fixed story: the main shock, the yearly recovery, regional differences, paid versus free admissions, and key findings. A line chart shows change over time. Regional bars make comparisons easy, while the map shows where differences occur. A grouped bar chart compares paid and free admissions.

The second part lets users choose regions, years and an attendance type. These filters update three KPIs and three charts without changing the fixed national story. Hover information gives values and site counts. Percentages help compare regional recovery without letting the largest attendance volumes dominate the comparison.

The app uses Streamlit, pandas and Plotly. I followed the recommended structure with `app.py`, `sections/` and `utils/`, and reused functions such as `load_data()`, `make_tables()`, `line_chart()`, `bar_chart()` and `map_chart()`. Data preparation is cached with `st.cache_data`. Dependency versions and installation instructions are provided in the repository. The app is deployed on Streamlit Community Cloud.

## 7. Limitations and next steps

The data is yearly. It cannot show monthly changes or the exact effects of reopening dates. Reporting coverage changes, and using the same sites does not control for opening days, exhibitions or changes in activity. Closure fields do not provide a reliable yearly opening calendar.

Regional differences could also reflect usual attendance changes. We cannot assume that every fall is a lasting effect of Covid. Regional resources may matter, but the dataset does not measure museum budgets or staffing. The results also do not show financial recovery or visitor satisfaction.

To go further, I would compare attendance with tourism data, museum opening periods, renovation projects and local economic information. This could help explain the remaining differences more clearly.

## 8. Conclusion

**French museums generally recovered in terms of recorded attendance by 2024.** The same 990 sites show a modest increase of 7.61% compared with 2019. However, recovery is not identical everywhere, and local closures can strongly affect small regional groups. The main lesson is to look at the overall recovery together with regional differences and data limitations.

## Sources

- [Ministry of Culture museum attendance dataset](https://www.data.gouv.fr/datasets/frequentation-des-musees-de-france-1), Open Licence.
- [Regional boundaries](https://www.data.gouv.fr/datasets/contours-administratifs), regions 2024, 1000 m; data.gouv.fr / IGN / OpenStreetMap contributors, ODbL 1.0.
- [Patrimostat 2025](https://www.culture.gouv.fr/content/download/378770/pdf_file/Patrimostat-2025.pdf), context on the MuMa renovation and the Approuague closure in 2023.
- [2024 information about the Arche closure](https://lheuredelest.org/que-faire-en-vacances-a-saint-pierre-et-miquelon/) and [the museum's practical information](https://www.arche-musee-et-archives.net/fr/10-infos-pratiques.html).

Source and licence details are also available in the [README](README.md). Context sources are not added as statistical series to the dashboard.
