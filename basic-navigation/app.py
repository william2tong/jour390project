import seaborn as sns
import faicons as fa
import plotly.express as px
import json

# Import data from shared.py
from shared import app_dir, foia_df, agency_abbreviations, agency_abbreviations_reverse, foia_collapsed_df

from shinywidgets import render_plotly
from shiny.express import input, render, ui


ui.page_opts(title="Shiny navigation components")

ui.nav_spacer()  # Push the navbar items to the right

footer = ui.input_select(
    "var", "Select variable", choices=["bill_length_mm", "body_mass_g"]
)

with ui.nav_panel("Page 1"):
    with ui.navset_card_underline(title="Penguins data", footer=footer):
        with ui.sidebar(open="desktop"):
    
            ui.input_selectize("agency", 
                            "Choose an agency",
                            list(agency_abbreviations_reverse.keys()),
                            selected=None,
                            )
            ui.input_select("view", 
                            "Choose view (hold shift to select multiple)",
                            ["General requests", 
                            "Dispositions",
                            "Processing Times", 
                            "Exemptions",
                            "Costs",
                            "Staff"],
                            multiple=True
                            )


with ui.nav_panel("Page 2"):
    "This is the second 'page'."



