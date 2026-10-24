"""Shared Plotly charts for the fixed story and the exploration section."""

import plotly.express as px
import streamlit as st

REGION_CODES = {
    "Guadeloupe": "01", "Martinique": "02", "Guyane": "03", "La Réunion": "04",
    "Mayotte": "06", "Île-de-France": "11", "Centre-Val de Loire": "24",
    "Bourgogne-Franche-Comté": "27", "Normandie": "28", "Hauts-de-France": "32",
    "Grand-Est": "44", "Pays-de-la-Loire": "52", "Bretagne": "53",
    "Nouvelle-Aquitaine": "75", "Occitanie": "76", "Auvergne-Rhône-Alpes": "84",
    "Provence-Alpes-Côte d'Azur": "93", "Corse": "94", "Saint-Pierre-et-Miquelon": "975",
}


def line_chart(table, label, key="story_line"):
    fig = px.line(table, x="annee", y="Admissions", markers=True,
                  hover_data=["Known_sites", "Observed_sites"],
                  labels={"annee": "Year", "Admissions": "Admissions (annual count)",
                          "Known_sites": "Sites with data", "Observed_sites": "Recorded sites"},
                  title=f"{label} over time", color_discrete_sequence=["#006D77"])
    fig.update_traces(connectgaps=False)
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(rangemode="tozero", tickformat=",.0f")
    for year in [2019, 2020, 2021, 2024]:
        if year in table["annee"].values:
            fig.add_vline(x=year, line_dash="dot", line_color="grey")
    st.plotly_chart(fig, width="stretch", key=key)


def bar_chart(table, label, start=2019, end=2024, key="story_bar"):
    values = table.dropna(subset=["Change_pct"]).sort_values("Change_pct")
    limit = max(1, float(values["Change_pct"].abs().max())) if not values.empty else 1
    fig = px.bar(values, x="Change_pct", y="region", orientation="h", color="Change_pct",
                 hover_data={"Before": ":,.0f", "After": ":,.0f", "Sites": True, "Change_pct": ":+.2f"},
                 labels={"region": "Region / territory", "Change_pct": "Change (%)",
                         "Before": f"{start} admissions", "After": f"{end} admissions", "Sites": "Same sites"},
                 title=f"{label}: change from {start} to {end} — same sites",
                 color_continuous_scale="BrBG", range_color=(-limit, limit), height=650)
    fig.add_vline(x=0, line_color="grey")
    fig.update_xaxes(title=f"Change from {start} to {end} (%)", ticksuffix="%")
    st.plotly_chart(fig, width="stretch", key=key)


def map_chart(table, geojson, label, start=2019, end=2024, key="story_map"):
    values = table.dropna(subset=["Change_pct"]).copy()
    values["code"] = values["region"].map(REGION_CODES)
    center, zoom = {"lat": 46.5, "lon": 2.5}, 4
    # Start over mainland France. For an overseas-only selection, use its real boundaries.
    if not values.empty and not values["code"].isin([c for c in REGION_CODES.values() if len(c) == 2 and int(c) >= 11]).any():
        points = []
        for feature in geojson["features"]:
            if feature["properties"]["code"] in values["code"].values:
                geometry = feature["geometry"]
                polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
                for polygon in polygons:
                    points.extend(polygon[0])
        if points:
            longitudes = [point[0] for point in points]
            latitudes = [point[1] for point in points]
            center = {"lon": (min(longitudes) + max(longitudes)) / 2,
                      "lat": (min(latitudes) + max(latitudes)) / 2}
            zoom = 5 if max(longitudes) - min(longitudes) < 6 else 1
    limit = max(1, float(values["Change_pct"].abs().max())) if not values.empty else 1
    fig = px.choropleth_map(
        values, geojson=geojson, featureidkey="properties.code", locations="code",
        color="Change_pct", hover_name="region",
        hover_data={"code": False, "Before": ":,.0f", "After": ":,.0f", "Sites": True, "Change_pct": ":+.2f"},
        labels={"Change_pct": "Change (%)", "Before": f"{start} admissions",
                "After": f"{end} admissions", "Sites": "Same sites"},
        color_continuous_scale="BrBG", range_color=(-limit, limit),
        map_style="white-bg", center=center, zoom=zoom,
        title=f"{label}: change from {start} to {end} — same sites", height=500,
    )
    fig.update_coloraxes(colorbar_ticksuffix="%")
    st.plotly_chart(fig, width="stretch", key=key)


def payment_chart(table):
    long = table.melt(id_vars=["annee", "Sites", "Free_share"], value_vars=["payant", "gratuit"],
                      var_name="Payment", value_name="Admissions")
    long["Payment"] = long["Payment"].map({"payant": "Paid", "gratuit": "Free"})
    fig = px.bar(long, x="annee", y="Admissions", color="Payment", barmode="group",
                 hover_data={"Admissions": ":,.0f", "Sites": True, "Free_share": ":.2f"},
                 labels={"annee": "Year", "Admissions": "Admissions (annual count)",
                         "Sites": "Same sites", "Free_share": "Free share (%)"},
                 title="Paid and free admissions, 2019–2024 — same compatible sites",
                 color_discrete_map={"Paid": "#4477AA", "Free": "#228833"})
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, width="stretch", key="story_payments")
