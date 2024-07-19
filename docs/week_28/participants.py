from dash import *
import dash_mantine_components as dmc
import requests
from dash_iconify import DashIconify


component = html.Div(
    [
        dmc.AvatarGroup(
            children=[
                dmc.Avatar(
                    src="https://avatars.githubusercontent.com/u/91216500?v=4",
                    radius="xl",
                ),
                dmc.Avatar(
                    src="https://avatars.githubusercontent.com/u/24227892?v=4",
                    radius="xl",
                ),
                dmc.Avatar(radius="xl"),
                dmc.Avatar("MK", color="cyan", radius="xl"),
                dmc.Avatar(
                    DashIconify(icon="radix-icons:star"), color="blue", radius="xl"
                ),
            ],
        ),
        dmc.Select(
            label="Select framework",
            placeholder="Select one",
            id="framework-select",
            value="ng",
            data=[
                {"value": "react", "label": "React"},
                {"value": "ng", "label": "Angular"},
                {"value": "svelte", "label": "Svelte"},
                {"value": "vue", "label": "Vue"},
            ],
            w=200,
            mb=10,
        ),
    ]
)
