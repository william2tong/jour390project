import faicons as fa
import plotly.express as px
import json
import pandas

# Load data and compute static values
from shared import app_dir, tips, foia_df, agency_abbreviations, agency_abbreviations_reverse, foia_collapsed_df
from shinywidgets import render_plotly


from shiny import reactive, render
from shiny.express import input, ui



# Add page title and sidebar
ui.page_opts(title="Federal FOIA Dashboard", fillable=True)

latest_year = 2024
years = [str(x) for x in list(range(2008, latest_year + 1))]

with ui.sidebar(open="desktop"):
    ui.input_selectize("agency", 
                       "Choose an agency",
                       list(agency_abbreviations_reverse.keys()),
                       selected=None,
                       )
    ui.input_select("view", 
                    "Choose view (hold ctrl or cmd to select multiple)",
                    ["General requests", 
                     "Dispositions",
                     "Processing Times", 
                     "Exemptions",
                     "Costs",
                     "Staff"],
                    multiple=True,
                    size=4
                    )
    # ui.input_select("compare", 
    #                 "Choose how to compare with other agencies",
    #                 {
    #                     "Requests": {"received_year": "Requests received", "processed_year": "Requests processed", "pending_start_year": "Start of year pending","pending_end_year": "End of year pending" },
    #                     "Disposition": {"duplicate_request": "Duplicate request",
    #                                     "full_denial": "Full denial",
    #                                     "full_grants": "Full grant",
    #                                     "improper_request_other_reason": "Improper request",
    #                                     "not_agency_record": "Not agency record",
    #                                     "other": "Other",
    #                                     "partially_granted": "Partially granted",
    #                                     "records_not_described": "Records not described",
    #                                     "referred_to_other_agency": "Referred to other agency",
    #                                     "withdrawn": "Withdrawn"},
    #                     "Processing Time": {"general_simple_average": "Average overall simple time",
    #                                         "general_complex_average": "Average overall complex time",
    #                                         "general_expedited_average": "Average overall expedited time",
    #                                         "granted_simple_average": "Average granted simple time",
    #                                         "granted_complex_average": "Average overall complex time",
    #                                         "granted_expedited_average": "Average overall complex time"}
    #                 },
    #                 multiple=False,
    #                 size=4
    #                 )
    ui.input_select("year", 
                    "Choose year for comparison",
                    years,
                    multiple=False,
                    size=4
                    )

# Add main content
ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}


    
with ui.layout_columns(fill=False):
    with ui.value_box(showcase=fa.icon_svg("clock")):
        @render.text
        def header2():
            if input.year():
                return f"Overall response times for {input.year()}"

        @render.express
        def general_request_times():
            if input.agency() and input.year():
                try:
                    f"Simple: {float(narrow_data()['general_simple_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])} | Complex: {float(narrow_data()['general_complex_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])}" 
                except:
                    f'No data for {input.year()}'
            

    with ui.value_box(showcase=fa.icon_svg("envelope-open-text")):
        @render.text
        def header3():
            if input.year():
                return f"Granted response time for {input.year()}"

        @render.express
        def granted_request_times():
            if input.agency() and input.year():
                try: 
                    f"Simple: {float(narrow_data()['granted_simple_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])} | Complex: {float(narrow_data()['granted_complex_average'].loc[narrow_data()['year'] == int(input.year())].iloc[0])}"
                except:
                    f'No data for {input.year()}'
            
            #f"{'true' if 'General requests' in input.view() else 'false'}"
            #f"{type(narrow_data_plot().loc[narrow_data_plot()['field'] == 'pending_start_year'])}"
            #f"{list(narrow_data_plot().loc[narrow_data_plot()['field'] == 'pending_start_year']['value'])}"

    with ui.value_box(showcase=ICONS["currency-dollar"]):
        @render.text
        def header4():
            if input.year():
                return f"Processing cost for {input.year()}"

        @render.express
        def processing_costs():
            if input.agency() and input.year():
                try:
                    f"${narrow_data()['processing_cost'][int(input.year())]:.2f}"
                except: 
                    f'No data for {input.year()}'


with ui.layout_columns(col_widths=[6, 6, 12]):
    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            @render.text
            def show_header1():
                if not input.view() or not input.agency():
                    return
                else:
                    if 'General requests' in list(input.view())[0]: 
                        return f'General request data'
                    elif 'Dispositions' in list(input.view())[0]:
                        return f'Disposition data'
                    elif 'Processing Times' in list(input.view())[0]:
                        return f'Processing time data'
                    elif 'Exemptions' in list(input.view())[0]:
                        return f'Exemption data'
                    elif 'Costs' in list(input.view())[0]:
                        return f'Cost data'
                    elif 'Staff' in list(input.view())[0]:
                        return f'Staff data'
                
        @render_plotly
        def lineplot1():
            if not input.view() or not input.agency():
                return
            ind = 0
            data = narrow_data_plot()
            data['value'] = data['value'].apply(pandas.to_numeric, errors='coerce')
            if 'General requests' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['pending_start_year', 'pending_end_year', 'received_year', 'processed_year'])]
            elif 'Dispositions' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['duplicate_request','fee_related,', 'full_denial','full_grants','improper_request_other_reason','not_agency_record','other','partially_granted','records_not_described','referred_to_other_agency', 'withdrawn'])]
            elif 'Processing Times' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['general_complex_average', 'general_simple_average', 'general_expedited_average', 'granted_complex_average', 'granted_simple_average', 'granted_expedited_average'])]
            elif 'Exemptions' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['exemption_1', 'exemption_2','exemption_3','exemption_4','exemption_5','exemption_6', 'exemption_7a', 'exemption_7b', 'exemption_7c','exemption_7d','exemption_7e', 'exemption_7f', 'exemption_8', 'exemption_9',])]
            elif 'Costs' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['litigation_cost', 'processing_cost', 'total_cost'])]
            elif 'Staff' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['total_staff'])]

            ecks = [] 
            for val in list(filtered_data['year']): 
                ecks.append(float(val))
            why = [] 
            for val in list(filtered_data['value']):
                why.append(float(val))
            cats = list(filtered_data['field'])

                       
            return px.line(
                filtered_data,
                x="year",
                y="value",
                color="field"
            )

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            @render.text
            def show_header2():
                if not input.view() or not input.agency():
                    return
                elif len(list(input.view())) == 1:
                    return
                else:
                    if 'General requests' in list(input.view())[1]: 
                        return f'General request data'
                    elif 'Dispositions' in list(input.view())[1]:
                        return f'Disposition data'
                    elif 'Processing Times' in list(input.view())[1]:
                        return f'Processing time data'
                    elif 'Exemptions' in list(input.view())[1]:
                        return f'Exemption data'
                    elif 'Costs' in list(input.view())[1]:
                        return f'Cost data'
                    elif 'Staff' in list(input.view())[1]:
                        return f'Staff data'
                
            
            
        
        @render_plotly
        def lineplot2():
            if not input.view() or not input.agency():
                return
            elif len(list(input.view())) == 1:
                return
            ind = 1
            data = narrow_data_plot()
            data['value'] = data['value'].apply(pandas.to_numeric, errors='coerce')
            if 'General requests' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['pending_start_year', 'pending_end_year', 'received_year', 'processed_year'])]
            elif 'Dispositions' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['duplicate_request','fee_related,full_denial','full_grants','improper_request_other_reason','not_agency_record','other','partially_granted','records_not_described','referred_to_other_agency', 'withdrawn'])]
            elif 'Processing Times' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['general_complex_average', 'general_simple_average', 'general_expedited_average', 'granted_complex_average', 'granted_simple_average', 'granted_expedited_average'])]
            elif 'Exemptions' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['exemption_1', 'exemption_2','exemption_3','exemption_4','exemption_5','exemption_6', 'exemption_7a', 'exemption_7b', 'exemption_7c','exemption_7d','exemption_7e', 'exemption_7f', 'exemption_8', 'exemption_9',])]
            elif 'Costs' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['litigation_cost', 'processing_cost', 'total_cost'])]
            elif 'Staff' in list(input.view())[ind]:
                filtered_data = data.loc[data['field'].isin(['total_staff'])]

            ecks = [] 
            for val in list(filtered_data['year']): 
                ecks.append(float(val))
            why = [] 
            for val in list(filtered_data['value']):
                why.append(float(val))
            cats = list(filtered_data['field'])

                       
            return px.line(
                filtered_data,
                x="year",
                y="value",
                color="field"
            )
#kind of takes up too much space anyway? also I need to work on dfir soooo 

# with ui.card(full_screen=True):
#     with ui.card_header(class_="d-flex justify-content-between align-items-center"):
#         @render.text
#         def header1():
#             if input.year() and input.agency() and input.compare():
#                 sorted = narrow_data_comp()
#                 sorted['value'] = sorted['value'].apply(pandas.to_numeric, errors='coerce')
#                 sorted = sorted.sort_values(by=['value'], ascending=False).copy() 

#                 return f"Ranking for {input.year()}: {sorted.values.to_list().index(agency_abbreviations_reverse(input.agency()))}"

#     @render.data_frame
#     def summary_statistics():
#         if not input.compare() or not input.year() or not input.agency():
#             return
#         sorted = narrow_data_comp()
#         sorted['value'] = sorted.apply(pandas.to_numeric, errors='coerce')
#         sorted = sorted.sort_values(by=['value'], ascending=False)

#         return render.DataGrid(sorted, filters=True)


ui.include_css(app_dir / "styles.css")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

@reactive.calc
def narrow_data():
    agency = input.agency()
    view = input.view()

    inter = foia_df[foia_df["agency"] == agency_abbreviations_reverse[agency]]

    return inter


@reactive.calc
def narrow_data_plot():
    agency = input.agency()
    ret = foia_collapsed_df.loc[foia_collapsed_df['agency'] == agency_abbreviations_reverse[agency]]
    return ret

@reactive.calc
def narrow_data_comp():
    comp = input.compare()
    year = int(input.year())
    ret = foia_collapsed_df.loc[foia_collapsed_df['field'] == comp] 
    ret = ret.loc[foia_collapsed_df['year'] == year]

    return ret

@reactive.calc
def get_mid_header(ind):
    
    if ind == 1 and len(input.view()) == 1:
        return None

    if 'General requests' in input.view()[ind]:
        return "General data about requests"
    elif 'Dispositions' in input.view()[ind]:
        return "Disposition data"
    elif 'Processing Times' in input.view()[ind]:
        return "Processing time data"
    elif 'Exemptions' in input.view()[ind]:
        return "Exemption data"
    elif 'Staff' in input.view()[ind]:
        return "Staff data"
    elif 'Costs' in input.view()[ind]:
        return "Cost data"
