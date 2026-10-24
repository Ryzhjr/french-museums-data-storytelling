"""Cleaning and simple calculations for the dashboard."""

import pandas as pd

INDICATORS = {"total": "Total admissions", "payant": "Paid admissions", "gratuit": "Free admissions"}


def number(value):
    return "Not available" if pd.isna(value) else f"{value:,.0f}"


def percent_change(current, baseline):
    if pd.isna(current) or pd.isna(baseline) or baseline <= 0:
        return None
    return float((current / baseline - 1) * 100)


def make_tables(df_raw):
    df = df_raw.copy()
    df["annee"] = pd.to_numeric(df["annee"], errors="raise").astype("Int64")
    for column in INDICATORS:
        df[column] = pd.to_numeric(df[column], errors="raise").astype("Int64")
    df["nom_du_musee"] = df["nom_du_musee"].str.strip()

    # Isolate every version of an ambiguous site-year, not just the second row.
    ambiguous = df.duplicated(["IDPatrimostat", "annee"], keep=False)
    complete = df[["payant", "gratuit", "total"]].notna().all(axis=1)
    mismatch = (complete & (df["payant"] + df["gratuit"] != df["total"])).fillna(False)
    quality = {
        "Original rows": len(df_raw),
        "Exact duplicate rows": int(df_raw.duplicated().sum()),
        "Ambiguous site-year groups": len(df.loc[ambiguous, ["IDPatrimostat", "annee"]].drop_duplicates()),
        "Excluded rows": int(ambiguous.sum()),
        "Paid/free/total mismatches": int(mismatch.sum()),
    }
    missing = pd.DataFrame({
        "Attendance field": list(INDICATORS.values()),
        "Missing values in original CSV": [int(df[c].isna().sum()) for c in INDICATORS],
    })
    # Keep published totals, including inconsistent payment sums. Never fill missing counts.
    return {"data": df.loc[~ambiguous].copy(), "quality": quality, "missing": missing}


def summarize(df, group, metric):
    return df.groupby(group).agg(
        Admissions=(metric, lambda values: values.sum(min_count=1)),
        Known_sites=(metric, "count"),
        Observed_sites=(metric, "size"),
    ).reset_index()


def common_sites(df, metric, start=2019, end=2024):
    """Match known values for the same sites at both dates."""
    before = df.loc[df["annee"] == start, ["IDPatrimostat", "region", metric]].dropna(subset=[metric])
    after = df.loc[df["annee"] == end, ["IDPatrimostat", metric]].dropna(subset=[metric])
    before = before.rename(columns={metric: "Before"})
    after = after.rename(columns={metric: "After"})
    return before.merge(after, on="IDPatrimostat", validate="one_to_one")


def regional_recovery(common, regions):
    """Both regional sums use exactly the same sites, including recorded zeros."""
    result = common.groupby("region").agg(
        Before=("Before", lambda values: values.sum(min_count=1)),
        After=("After", lambda values: values.sum(min_count=1)),
        Sites=("IDPatrimostat", "count"),
    ).reindex(regions)
    result["Sites"] = result["Sites"].fillna(0).astype(int)
    # A zero first-year reference has no percentage change; it is not a zero change.
    result["Change_pct"] = (result["After"] / result["Before"].replace(0, pd.NA) - 1) * 100
    result["Difference"] = result["After"] - result["Before"]
    return result.rename_axis("region").reset_index()


def payment_comparison(df):
    """Use a fixed set of sites with coherent payment counts in all six years."""
    years = list(range(2019, 2025))
    complete = df[["payant", "gratuit", "total"]].notna().all(axis=1)
    compatible = complete & (df["payant"] + df["gratuit"] == df["total"])
    rows = df.loc[compatible & df["annee"].isin(years)].copy()
    counts = rows.groupby("IDPatrimostat")["annee"].nunique()
    rows = rows[rows["IDPatrimostat"].isin(counts[counts == len(years)].index)]
    annual = rows.groupby("annee")[["payant", "gratuit", "total"]].sum(min_count=1)
    annual["Sites"] = rows.groupby("annee")["IDPatrimostat"].nunique()
    annual["Free_share"] = annual["gratuit"] / annual["total"].replace(0, pd.NA) * 100
    return annual.reset_index()
