import plotly.express as px
import json
import pandas

# Load data and compute static values
from shared import app_dir, chicago_df, chicago_facility_types, la_df, la_facility_types, nyc_facility_types, nyc_df
from shinywidgets import render_plotly
from functools import partial

from shiny import reactive, render
from shiny.express import input, ui
from shiny.ui import page_navbar

latest_year = 2025
years = [str(x) for x in list(range(2010, latest_year + 1))]


# Add page title and sidebar
ui.page_opts(title="Food establishment inspections", fillable=False, page_fn=partial(page_navbar, id="page"))

with ui.nav_panel("City search"):
    with ui.layout_sidebar():
        with ui.sidebar(open="desktop"):
            
            ui.input_select("city", 
                            "Choose city",
                            ["Chicago", 
                             "New York",
                             "Los Angeles"
                            ],
                            multiple=False,
                            size=3
            )
            @render.express
            def year_selection():

                if "Los Angeles" in input.city():
                    selected = "2015"
                else: 
                    selected = "2019"
                ui.input_select("year", 
                                "Choose year",
                                get_years(),
                                multiple=False,
                                selected=selected,
                                size=4
                                )
            @render.express
            def facility_selection():
                selected = ""
                if "Chicago" in input.city():
                    selected = "Restaurant"

                elif "New York" in input.city():
                    selected = "Pizza"
                ui.input_selectize("type",
                        "Choose facility type",
                        facility_type(),
                        selected=selected,
                        multiple=False,
                )
            
            
        with ui.layout_columns(full_screen=True):
            with ui.card(full_screen=True):
                with ui.card(full_screen=True):
                    @render.express
                    def flourish_graph():
                        if input.city():
                            if "Chicago" in input.city(): 
                                ui.HTML("<iframe src='https://flo.uri.sh/visualisation/23646055/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:450px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/23646055/?utm_source=embed&utm_campaign=visualisation/23646055' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>")
                            elif "New York" in input.city():
                                ui.HTML("<iframe src='https://flo.uri.sh/visualisation/23678234/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/23678234/?utm_source=embed&utm_campaign=visualisation/23678234' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>")
                            elif "Los Angeles" in input.city():
                                ui.HTML("<iframe src='https://flo.uri.sh/visualisation/23678259/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/23678259/?utm_source=embed&utm_campaign=visualisation/23678259' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>")
            with ui.card(full_screen=True):
                with ui.card_header(class_="d-flex justify-content-between align-items-center"):
                    @render.text
                    def header5():
                        if not input.city() or not input.year() or not input.type():
                            return "N/A"
                        else:
                            return f"{input.city()} | {input.year()} | {input.type()}"
                    

                    
                @render_plotly
                def lineplot3():
                    ui.remove_ui(selector="[class='lm-Widget p-Widget js-plotly-plot']", multiple=True, immediate=True)
                    
                    filtered_df = get_df()
                    

                    pie = px.pie(filtered_df, values='count', names='result', title='Proportion of results')
                    
                    pie.update_layout(legend=dict(orientation="h",))
                    return pie
                        
            
# with ui.nav_panel("Individual Agencies"): 
#     with ui.layout_sidebar():
#         with ui.sidebar(open="desktop"):
#             available_agencies = list(agency_abbreviations_reverse.keys())
#             available_agencies.remove("Department of Defense")
#             ui.input_selectize("agency", 
#                             "Choose an agency (backspace first before searching )",
#                             available_agencies,
#                             selected=None,
#                             )
#             ui.input_select("year", 
#                             "Choose year for top-level display",
#                             years,
#                             multiple=False,
#                             size=4
#                             )
#             ui.input_select("view", 
#                             "Choose view",
#                             ["General requests", 
#                             "Dispositions",
#                             "Processing Times", 
#                             "Exemptions",
#                             "Costs",
#                             "Staff"],
#                             multiple=False,
#                             size=4
#                             )
#             # ui.input_select("compare", 
#             #                 "Choose how to compare with other agencies",
#             #                 {
#             #                     "Requests": {"received_year": "Requests received", "processed_year": "Requests processed", "pending_start_year": "Start of year pending","pending_end_year": "End of year pending" },
#             #                     "Disposition": {"duplicate_request": "Duplicate request",
#             #                                     "full_denial": "Full denial",
#             #                                     "full_grants": "Full grant",
#             #                                     "improper_request_other_reason": "Improper request",
#             #                                     "not_agency_record": "Not agency record",
#             #                                     "other": "Other",
#             #                                     "partially_granted": "Partially granted",
#             #                                     "records_not_described": "Records not described",
#             #                                     "referred_to_other_agency": "Referred to other agency",
#             #                                     "withdrawn": "Withdrawn"},
#             #                     "Processing Time": {"general_simple_average": "Average overall simple time",
#             #                                         "general_complex_average": "Average overall complex time",
#             #                                         "general_expedited_average": "Average overall expedited time",
#             #                                         "granted_simple_average": "Average granted simple time",
#             #                                         "granted_complex_average": "Average overall complex time",
#             #                                         "granted_expedited_average": "Average overall complex time"}
#             #                 },
#             #                 multiple=False,
#             #                 size=4
#             #                 )
            
#         with ui.layout_columns(fill=False):
#             with ui.value_box(showcase=fa.icon_svg("clock")):
#                 @render.text
#                 def header2():
#                     if input.year():
#                         return f"Overall response times for {input.year()}"

#                 @render.express
#                 def general_request_times():
#                     if input.agency() and input.year():
#                         try:
#                             f"Simple: {float(narrow_data()['general_simple_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])} | Complex: {float(narrow_data()['general_complex_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])}" 
#                         except:
#                             f'No data for {input.year()}'
                    

#             with ui.value_box(showcase=fa.icon_svg("envelope-open-text")):
#                 @render.text
#                 def header3():
#                     if input.year():
#                         return f"Granted response time for {input.year()}"

#                 @render.express
#                 def granted_request_times():
#                     if input.agency() and input.year():
#                         try: 
#                             f"Simple: {float(narrow_data()['granted_simple_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])} | Complex: {float(narrow_data()['granted_complex_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])}"
#                         except:
#                             f'No data for {input.year()}'
                    
#                     #f"{'true' if 'General requests' in input.view() else 'false'}"
#                     #f"{type(narrow_data_plot().loc[narrow_data_plot()['field'] == 'pending_start_year'])}"
#                     #f"{list(narrow_data_plot().loc[narrow_data_plot()['field'] == 'pending_start_year']['value'])}"

#             with ui.value_box(showcase=fa.icon_svg("dollar-sign")):
#                 @render.text
#                 def header4():
#                     if input.year():
#                         return f"Processing cost for {input.year()}"

#                 @render.express
#                 def processing_costs():
#                     if input.agency() and input.year():
#                         try:
#                             f"${float(narrow_data()['processing_cost'].loc[narrow_data()['year'] == int(input.year())].iloc[0]):.2f}"
#                         except: 
#                             f'No data for {input.year()}'

        
    


#         # with ui.layout_columns(col_widths=[6, 6, 12]):
#         with ui.card(full_screen=True):
#             with ui.card_header(class_="d-flex justify-content-between align-items-center"):
#                 @render.text
#                 def show_header1():
#                     if not input.view() or not input.agency():
#                         return
#                     else:
#                         if 'General requests' in input.view(): 
#                             return f'General request data'
#                         elif 'Dispositions' in input.view():
#                             return f'Disposition data'
#                         elif 'Processing Times' in input.view():
#                             return f'Processing time data'
#                         elif 'Exemptions' in input.view():
#                             return f'Exemption data'
#                         elif 'Costs' in input.view():
#                             return f'Cost data'
#                         elif 'Staff' in input.view():
#                             return f'Staff data'
            
#             @render_plotly
#             def lineplot1():
#                 if not input.view() or not input.agency():
#                     return
#                 ui.remove_ui(selector="[class='lm-Widget p-Widget js-plotly-plot']", multiple=True, immediate=True)
#                 data = narrow_data_plot()
#                 data['value'] = data['value'].apply(pandas.to_numeric, errors='coerce')
#                 lbls = {}
#                 if 'General requests' in input.view():
#                     filtered_data = data.loc[data['field'].isin(["Pending at year end", "Pending at year start", 'Received', 'Processed'])]
#                     lbls = {"year": "Fiscal year", 
#                             "Value": "Number of requests", 
#                             "field": "Key"
#                             }
#                 elif 'Dispositions' in input.view():
#                     filtered_data = data.loc[data['field'].isin(['duplicate_request','fee_related,', 'full_denial','full_grants','improper_request_other_reason','not_agency_record','other','partially_granted','records_not_described','referred_to_other_agency', 'withdrawn'])]
#                     lbls = {"year": "Fiscal year", 
#                             "Value": "Number of requests", 
#                             "field": "Key"
#                             }
#                 elif 'Processing Times' in input.view():
#                     filtered_data = data.loc[data['field'].isin(['general_complex_average', 'general_simple_average', 'general_expedited_average', 'granted_complex_average', 'granted_simple_average', 'granted_expedited_average'])]
#                     lbls = {"year": "Fiscal year", 
#                             "Value": "Number of requests", 
#                             "field": "Key"
#                             }
#                 elif 'Exemptions' in input.view():
#                     filtered_data = data.loc[data['field'].isin(['exemption_1', 'exemption_2','exemption_3','exemption_4','exemption_5','exemption_6', 'exemption_7a', 'exemption_7b', 'exemption_7c','exemption_7d','exemption_7e', 'exemption_7f', 'exemption_8', 'exemption_9',])]
#                     lbls = {"year": "Fiscal year", 
#                             "Value": "Number of requests", 
#                             "field": "Key"
#                             }
#                 elif 'Costs' in input.view():
#                     filtered_data = data.loc[data['field'].isin(['litigation_cost', 'processing_cost', 'total_cost'])]
#                     lbls = {"year": "Fiscal year", 
#                             "Value": "Number of requests", 
#                             "field": "Key"
#                             }
#                 elif 'Staff' in input.view():
#                     filtered_data = data.loc[data['field'].isin(['total_staff'])]
#                     lbls = {"year": "Fiscal year", 
#                             "Value": "Number of requests", 
#                             "field": "Key"
#                             }
                
#                 graph = px.line(
#                     filtered_data,
#                     x="year",
#                     y="value",
#                     color="field",
#                     labels=lbls
#                 )

#                 graph.update_layout(legend=dict(entrywidth=0.05, entrywidthmode="fraction", font=dict(size=8), itemwidth=30))
#                 return graph


# ui.include_css(app_dir / "styles.css")

# # --------------------------------------------------------
# # Reactive calculations and effects
# # --------------------------------------------------------



@reactive.calc
def page1_graph():
    if not input.view0():
        return
    elif 'General requests' in input.view0():
        filtered_data = overall_quarterly_df

        return px.line(
            filtered_data,
            x="FY with decimal",
            y="Value",
            color="Field",
            labels={"FY with decimal": "Fiscal year and quarter", "Value": "Number of requests", "Field": "Key"}
        )
    elif 'Staff vs. processing time' in input.view0():
        if not input.staffing_view():
            return
        else: 
            filtered_data = foia_df[['total_staff', str(input.staffing_view())]]
            filtered_data[str(input.staffing_view())] = filtered_data[input.staffing_view()].apply(pandas.to_numeric, errors='coerce')
            return px.scatter(
                filtered_data,
                x="total_staff",
                y=str(input.staffing_view()),
                labels={"total_staff": "Total Staff"}
            )


@reactive.calc
def get_df():
    if not input.city():
        return
    df = None
    filtered_df = None
    if "Chicago" in input.city():
        df = chicago_df
       
    elif "Los Angeles" in input.city():
        df =  la_df
    elif "New York" in input.city():
        df = nyc_df
    
    filtered_df = df[(df['facility_type'] == input.type())]
    filtered_df = filtered_df[filtered_df['year'] == int(input.year())]
    if filtered_df is not None:
        return filtered_df

@reactive.calc
def facility_type():
    if not input.city():
        return
    if "Chicago" in input.city():
        return chicago_facility_types
    elif "Los Angeles" in input.city():
        return la_facility_types
    elif "New York" in input.city():
        return nyc_facility_types
    
@reactive.calc
def get_years():
    if not input.city():
        return
    if "Chicago" in input.city():
        return [str(x) for x in list(range(2010, 2026))]
    elif "Los Angeles" in input.city():
        return [str(x) for x in list(range(2015, 2019))]
    elif "New York" in input.city():
        return [str(x) for x in list(range(2015, 2026))]
    