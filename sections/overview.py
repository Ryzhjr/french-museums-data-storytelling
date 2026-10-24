import pandas as pd
import streamlit as st
from utils.prep import INDICATORS, common_sites, number, percent_change, regional_recovery, summarize
from utils.viz import line_chart, bar_chart, map_chart


def show_overview(annual):
    values = annual.set_index("annee")
    totals = values["Admissions"]
    changes = totals.pct_change(fill_method=None).mul(100)
    st.subheader("1. The Big Picture - The COVID Shock")
    c1, c2, c3 = st.columns(3)
    c1.metric("2019 - Before the pandemic", number(totals.loc[2019]))
    c2.metric("2020 - The crisis", number(totals.loc[2020]))
    c3.metric("2024 - The outcome", number(totals.loc[2024]))
    st.write("These three KPIs give a quick view of the COVID-period shock and the return of visits after lockdowns. "
             f"Recorded admissions fell by **{abs(changes.loc[2020]):.2f}%** in 2020. "
             f"By 2024, they were **{percent_change(totals.loc[2024], totals.loc[2019]):+.2f}%** above 2019. "
             "The large fall matches the period of lockdowns and museum closures. The curve below shows how the recovery happened.")
    st.caption("We keep all available records each year, including recorded zeros, to follow activity before, during and after the crisis. "
               f"Sites with known counts: {number(values.loc[2019, 'Known_sites'])} in 2019, "
               f"{number(values.loc[2020, 'Known_sites'])} in 2020 and {number(values.loc[2024, 'Known_sites'])} in 2024. "
               "Some sites may have closed during the crisis. Closures are part of the story, but missing records can also come from reporting gaps. "
               "We cannot assume that every missing site closed because of COVID. The regional analysis separately compares the same sites.")

    st.subheader("2. Attendance Evolution - Understanding the Recovery")
    line_chart(annual, "Total admissions", key="story_line")
    st.markdown("**2014-2019: changes before the crisis**")
    st.write(f"Before COVID, attendance changed from year to year, but stayed around a similar overall level. "
             f"It fell by **{abs(changes.loc[2015]):.2f}%** in 2015 and **{abs(changes.loc[2016]):.2f}%** in 2016, "
             f"to **{number(totals.loc[2016])}** admissions. It then rose by **{changes.loc[2017]:.2f}%** in 2017 "
             f"and **{changes.loc[2018]:.2f}%** in 2018. The 2019 change was small ({changes.loc[2019]:+.2f}%). "
             f"Overall, 2019 was **{percent_change(totals.loc[2019], totals.loc[2014]):+.2f}%** above 2014.")
    st.write("**Possible explanation:** the attacks in France in 2015 and 2016, and stronger security under the Vigipirate plan, "
             "may have affected tourism and visits to cultural places. Some people may have felt less willing to travel or go out. "
             "This is a possible link with the falls on the curve, not a cause proved by our museum data.")

    st.markdown("**2020-2021: a sharp fall, then a partial return**")
    loss = totals.loc[2019] - totals.loc[2020]
    st.write(f"The curve falls sharply in 2020, with **{number(loss)} fewer admissions** than in 2019. "
             "France's first lockdown began in March 2020. Museums closed, travel was restricted and international tourism fell. "
             "There were far fewer opportunities to visit museums during this period.")
    st.write(f"In 2021, attendance started to rise again: **{changes.loc[2021]:.2f}%** above 2020, "
             f"reaching **{number(totals.loc[2021])}** admissions. Museums reopened as vaccination progressed and some restrictions eased. "
             f"However, the count was still **{abs(percent_change(totals.loc[2021], totals.loc[2019])):.2f}%** below 2019. "
             "The first return was therefore limited: 2020 and 2021 both remained very low compared with the pre-crisis level.")

    st.markdown("**2022: a strong rebound, but not yet back to 2019**")
    st.write(f"Between 2021 and 2022, admissions rose by **{changes.loc[2022]:.2f}%**, to **{number(totals.loc[2022])}**. "
             "Restrictions were eased further and the vaccine pass was suspended in 2022. These changes made cultural visits easier. "
             f"The recorded count was again close to the pre-COVID years, but still **{abs(percent_change(totals.loc[2022], totals.loc[2019])):.2f}%** below 2019.")
    st.write("**Hypothesis:** even after restrictions were lifted, people may have needed more time to return to their usual habits. "
             "This could help explain why the full return was not immediate. Our data do not measure this adjustment time or visitor motives.")

    st.markdown("**2023: the recorded count passes the 2019 level**")
    st.write(f"Between 2022 and 2023, attendance increased again, by **{changes.loc[2023]:.2f}%**, "
             f"to **{number(totals.loc[2023])}** admissions. This was the first year after the crisis with a recorded count above 2019. "
             "The earlier falls had now been passed in the combined annual total.")
    st.write("**Hypothesis:** fewer health restrictions and the return of tourism may have supported this rise. "
             "People may also have wanted to enjoy outings again after a difficult period. These ideas could help explain the recovery, "
             "but the annual counts do not show how much each factor contributed.")

    st.markdown("**2024: a further rise, at a slower pace**")
    st.write(f"Between 2023 and 2024, admissions increased by **{changes.loc[2024]:.2f}%**, to **{number(totals.loc[2024])}**. "
             "The curve still rises, but less sharply than in the previous recovery years. "
             "The 2024 count is higher than every annual count from 2014 to 2019 in this file, "
             f"but it is only **{percent_change(totals.loc[2024], totals.loc[2019]):+.2f}%** above 2019. "
             "This difference is much smaller than the rebound from the crisis lows. It is not enough on its own to conclude "
             "that people have made a large, lasting change in their museum habits.")
    st.caption("The historical context helps us read the curve, but the CSV cannot prove each cause. "
               "Coverage also changes between years; hover to see known site counts. The four unclear records excluded in 2021 lower that year's total.")
    st.write("The national total has returned. We now compare the same sites across regions to see whether this recovery was shared.")


def show_exploration(df, boundaries, regions, date_range, metric):
    start, end = date_range
    annual = summarize(df, "annee", metric).set_index("annee").reindex(range(start, end + 1))
    first, last = annual.loc[start, "Admissions"], annual.loc[end, "Admissions"]
    change = percent_change(last, first) if start != end else None
    known = annual.loc[end, "Known_sites"]
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{INDICATORS[metric]} - {end}", number(last))
    c2.metric(f"Observed change - {start} to {end}", "Not available" if change is None else f"{change:+.2f}%")
    c3.metric(f"Sites with known values - {end}", "0" if pd.isna(known) else number(known))
    st.caption("Observed totals use each year's available records. Missing values are not zeros. "
               "The endpoint percentage needs two different years and a positive first-year total.")
    if df.empty:
        st.info("No records match this selection. Choose at least one region and a period with data.")
        return
    line_chart(annual.reset_index(), INDICATORS[metric], key="explore_line")
    if start == end:
        st.info("Choose at least two different years to compare regional changes.")
        return
    regional = regional_recovery(common_sites(df, metric, start, end), regions)
    if regional["Change_pct"].notna().sum() == 0:
        st.info("No valid regional endpoint percentage: shared known values and a positive first-year total are needed.")
        return
    st.caption(f"Regional comparison: {start} to {end}, using the same sites with known values at both dates. "
               "The bars and map share one percentage scale. Hover for counts and sample sizes.")
    bar_chart(regional, INDICATORS[metric], start, end, key="explore_bar")
    map_chart(regional, boundaries, INDICATORS[metric], start, end, key="explore_map")
