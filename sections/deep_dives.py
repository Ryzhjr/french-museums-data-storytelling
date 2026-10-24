import streamlit as st
from utils.prep import INDICATORS, number, percent_change
from utils.viz import bar_chart, map_chart, payment_chart


def show_deep_dives(tables):
    regional = tables["by_region"].dropna(subset=["Change_pct"])
    st.subheader("3. Regional Recovery - Not All Regions Recovered Equally")
    st.write(f"We now follow the same **{len(tables['common']):,} sites** with known total admissions in 2019 and 2024. "
             "The number of sites in the dataset changes from year to year. Keeping the same sites makes the comparison fairer. "
             "Each region keeps its own fixed list. The bars show percentage change; hover also gives the two volumes and the number of sites.")
    bar_chart(regional, "Total admissions", key="story_bar")
    st.write("**Did museums recover after Covid? Overall, yes.** The national curve shows the major break in 2020. "
             "Here, we compare 2019 with 2024, five years between the two dates. Across the same 990 sites, "
             "admissions rise from **63,471,160** to **68,303,209**, or **+7.61%**. "
             "By 2024, attendance is back to a level close to before Covid, with a modest overall increase. "
             "But the recovery is not the same everywhere. Several regions show fairly small changes, while others show larger gaps. "
             "These two dates alone cannot tell us whether the changes are usual yearly variations.")
    largest = regional.loc[regional["After"].idxmax()]
    fastest = regional.loc[regional["Change_pct"].idxmax()]
    lower = regional.loc[regional["region"].eq("Nouvelle-Aquitaine")].iloc[0]
    st.write(f"**More visits does not always mean faster growth.** {largest['region']} records "
             f"**{number(largest['After'])} admissions** across **{int(largest['Sites'])} sites**, "
             f"with **{largest['Change_pct']:+.2f}%** since 2019. {fastest['region']} has fewer visits "
             f"(**{number(fastest['After'])}**, across **{int(fastest['Sites'])} sites**), "
             f"but a stronger rise: **{fastest['Change_pct']:+.2f}%**.")
    below = int((regional["Change_pct"] < 0).sum())
    st.write(f"Some regions rise and others fall: **{below} of {len(regional)}** remain below 2019. "
             f"For example, {lower['region']} records **{lower['Change_pct']:+.2f}%**. "
             "Some differences could reflect usual changes in museum attendance, rather than Covid alone. "
             "Maybe some regions also had more money or staff to restart activities after the crisis. "
             "The dataset does not measure these resources.")
    st.write("**Local situations help explain the largest falls.** We checked online information after noticing unusual results. "
             "In Mayotte, the MuMa falls from **6,583 admissions to zero (-100.00%)** in 2024. "
             "Published reports describe its closure to the public for renovation, while some activities continued outside the museum. "
             "In Saint-Pierre-et-Miquelon, the Arche falls from **4,303 to 171 admissions (-96.03%)**; "
             "information for 2024 reports a closure for building works. These local situations help us understand the falls "
             "without linking them directly to Covid. Each territory has just **one museum** in our comparison, "
             "so a problem at that site can cause a very large percentage fall for the whole territory.")
    st.write("In Guyane, the Approuague ecomuseum closed in 2023 and reports **zero admissions in the 2024 CSV**.")
    map_chart(regional, tables["boundaries"], "Total admissions", key="story_map")
    st.caption("The map uses exactly the same percentages and scale as the bars. Brown: below 2019; teal: above 2019. "
               "Uncoloured areas have no valid comparison. Zoom out and drag to see overseas territories. "
               "Boundaries: data.gouv.fr / IGN / OpenStreetMap contributors, 2024, 1000 m, ODbL 1.0; licence links in README.")
    st.write("**Why percentages?** Île-de-France has major cultural collections and very high attendance. "
             "Visit numbers alone would mainly show these differences in size. Percentages compare each region with its own "
             "2019 level, making recovery easier to compare. Large percentages still need care when very few museums are involved.")


def show_payments(annual):
    st.subheader("4. Paid vs Free Admissions - Did the Recovery Change?")
    if annual.empty:
        st.info("No complete fixed payment panel is available.")
        return
    values = annual.set_index("annee")
    before, after = values.loc[2019], values.loc[2024]
    count = int(before["Sites"])
    st.write(f"This section uses a separate fixed group of **{count} sites**, with paid, free and total counts "
             "in every year from 2019 to 2024. Every record must satisfy paid plus free equals the published total. "
             "The payment panel is smaller than the regional panel; its totals must not be mixed with the national KPIs.")
    payment_chart(annual)
    paid_change = percent_change(after["payant"], before["payant"])
    free_change = percent_change(after["gratuit"], before["gratuit"])
    paid_fall = percent_change(values.loc[2020, "payant"], before["payant"])
    free_fall = percent_change(values.loc[2020, "gratuit"], before["gratuit"])
    st.write("In 2019, paid admissions were higher than free admissions. Both fell sharply during the lockdown period, "
             "but free admissions fell less than paid admissions compared with 2019. "
             "This made the gap smaller in 2020 and 2021. Maybe tourists are more likely to visit paid museums, "
             "so fewer tourists could mean fewer paid visits. Some people in France may also have received only part of their usual income "
             "during lockdowns, making free visits more attractive when museums reopened.")
    difference = after["Free_share"] - before["Free_share"]
    last_change = percent_change(after["gratuit"], values.loc[2023, "gratuit"])
    st.write("Both increased again in 2022 and 2023. In 2024, paid admissions continued to rise, while free admissions fell. "
             "The gap became larger again after Covid, suggesting that the change during the crisis was mainly temporary.")


def show_quality(tables, filtered, metric):
    st.subheader("Data Quality")
    q = tables["quality"]
    st.write("We cleaned the dataset before our analysis. We read the CSV using UTF-8 to keep accents in museum and region names correct. "
            f"The original CSV contains {q['Original rows']:,} rows. We removed {q['Excluded rows']} unclear rows, "
            f"leaving {len(tables['data']):,} rows. We also found 3 missing values for total admissions and "
            f"{q['Paid/free/total mismatches']} cases where paid plus free admissions did not match the published total. "
            "We kept the original values without inventing missing data.")
    st.subheader("Limitations")
    st.write("The number of museums changes between years, so national totals do not always represent the same museums. "
            f"For regional comparisons, we used the same {len(tables['common']):,} museums in 2019 and 2024 "
            "to make the results more reliable.")
    st.write("The dataset only contains yearly information. We cannot study monthly changes or the exact effects "
            "of lockdowns and reopening dates.")
    st.write("Finally, the dataset does not always explain why attendance increased or decreased. Museum renovations, "
            "tourism and economic conditions may influence the results, but we would need more information to confirm these explanations.")
