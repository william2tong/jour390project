import seaborn as sns
from faicons import icon_svg
import re
import textwrap

# Import data from shared.py
from shared import app_dir, dfs, agency_status

from shiny import reactive
from shiny.express import input, render, ui



ui.page_opts(title="Chicago FOIA dashboard", fillable=True)


with ui.sidebar(title="Filter controls"):

    ui.input_select(
        "agency",
        "Choose an agency:",
        [
            "None",
            "Public Health Department",
            "Business Affairs and Consumer Protection Department",
            "Finance Department",
            "Procurement Services Department"
        ],
    )

    "Note: Finance Department status data came as exemption labels. Exemptions may have accompanied partial disclosure, and no exemptions doesn't automatically imply full request grant."
    

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("building-columns")):
        "Number of requests"


        @render.text
        def count():
            if type(filtered_df()) == str:
                return 'N/A'

            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("clock")):
        "Average completion time"


        @render.text
        def avg_completion_time():

            if type(filtered_df()) == str:
                return 'N/A'

            converted = []
            for s in filtered_df()['Completion Time']:
                if re.fullmatch('^\d*\.?\d*$', str(s)):
                    converted.append(float(s))
            if converted == []:
                converted.append(-1)

            return f"{(sum(converted)/len(converted)):.1f} days"

    
    with ui.value_box(showcase=icon_svg("envelope")):
        "Most Common Response"

        @render.text
        def common_status():

            if type(filtered_df()) == str:
                return 'N/A'

            freq_dict = {'placeholder': -1}

            highest = 'placeholder'
            for s in filtered_df()['Request Status']: 
                if s not in freq_dict.keys():
                    freq_dict[s] = 0
                freq_dict[s] += 1
                if freq_dict[s] > freq_dict[highest]:
                    highest = s

            return f'{freq_dict[highest]} "{highest}"'
    


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Types of dispositions")

        @render.plot
        def length_depth():

            if type(filtered_df()) == str:
                return

            plot = sns.barplot(
                data=agency_status[agency_status['Agency'] == input.agency()],
                x="Status",
                y="Number",
                #hue="Status",
            )

            #read off google's ai generated code because other top search results weren't getting at this question 
            plot.bar_label(plot.containers[0])
            labels = [textwrap.fill(label.get_text(), 10) for label in plot.get_xticklabels()]
            plot.set_xticklabels(labels, fontsize=5)

            

            return plot

    with ui.card(full_screen=True):
        ui.card_header("Request data")

        @render.data_frame
        def summary_statistics():

            if type(filtered_df()) == str:
                return
            cols = [
                "Customer Full Name",
                "Company Name",
                "Create Date",
                "Summary",
                "Close Date",
                "Completion Time",
                "Request Status"
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


ui.include_css(app_dir / "styles.css")

@reactive.calc
def filtered_df():
    #filt_df = df[df["species"].isin(input.species())]
    
    agency_name = input.agency()
    
    filt_df = dfs[agency_name]
    #filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
