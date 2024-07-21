from dash import *
import dash_mantine_components as dmc
import requests
from dash_iconify import DashIconify


component = html.Div(
    [
        dmc.AvatarGroup(
            children=[
                dmc.Tooltip(
                    label="Mike_Purtell",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(
                    src="https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/mike_purtell/288/21990_2.png",
                    radius="xl",
                )]
                ),

            ],
        ),
        # dmc.Select(
        #     label="Select framework",
        #     placeholder="Select one",
        #     id="framework-select",
        #     value="ng",
        #     data=[
        #         {"value": "react", "label": "React"},
        #         {"value": "ng", "label": "Angular"},
        #         {"value": "svelte", "label": "Svelte"},
        #         {"value": "vue", "label": "Vue"},
        #     ],
        #     w=200,
        #     mb=10,
        # ),
    ]
)