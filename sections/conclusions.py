import streamlit as st
from utils.prep import percent_change


def show_conclusions(tables):
    st.subheader("5. What Did We Learn? - Key Findings")
    common = tables["common"]
    regional = tables["by_region"].dropna(subset=["Change_pct"])
    below = int((regional["Change_pct"] < 0).sum())
    growth = percent_change(common["After"].sum(), common["Before"].sum())
    payments = tables["payments"].set_index("annee")
    st.success("**Overall, French museums recovered after Covid.**")
    st.write("The pandemic caused a major drop in attendance in 2020, "
             "but visits increased again from 2021. By 2024, attendance had returned to its pre-Covid level, "
             f"with even a small increase of **{growth:.2f}%** for the same {len(common):,} museums.\n\n"
             "**The recovery was not exactly the same everywhere.** Some regions recorded small increases, while others recorded "
             "small decreases. These differences can also be normal changes in museum attendance, not necessarily long-term effects "
             "of Covid. We can also imagine that regions with more financial resources recovered more easily.\n\n"
             "**Some large decreases had other possible explanations.** In a few territories, we found particular situations, "
             "such as museum closures or renovations, which could explain the very low numbers.\n\n"
             "**Paid and free admissions also changed during the crisis.** Their gap became smaller in 2020 and 2021, "
             "before increasing again after Covid. In 2024, free admissions were higher than in 2019, but their share was slightly lower.\n\n"
             "**In conclusion, the museums generally recovered from the Covid crisis.** The data shows a small overall increase, "
             "but not a major long-term change in attendance. To better understand the remaining differences, we could study tourism, "
             "local economic conditions and museum renovations.")
