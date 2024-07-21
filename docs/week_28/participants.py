from dash import *
import dash_mantine_components as dmc
import requests
from dash_iconify import DashIconify
from dash_ace import DashAceEditor

pipinstallpython = example_code = """from dash import *
import dash_ag_grid as dag
import dash_leaflet as dl
import pandas as pd
import geopandas as gpd
import dash_mantine_components as dmc
import json
from dash_extensions.javascript import arrow_function, assign
#########################################
# Setup data and format for the map data, borders & cluster
#########################################

# Define the file path for data
file_path = '2024/week-28/Superstore_with_LAT_LNG.xlsx'

# Read the Excel file
df = pd.read_excel(file_path)

# Get unique State/Province values
unique_states = df['State/Province'].unique()

# Create data for Select component
state_select_data = [{"label": "Everything", "value": "Everything"}] + [
    {"label": state, "value": state} for state in sorted(unique_states)
]

# Create a dictionary mapping state/province to region
state_to_region = pd.Series(df.Region.values, index=df['State/Province']).to_dict()

# Convert any Timestamp columns to strings
for column in df.select_dtypes(include=['datetime', 'datetime64[ns]']):
    df[column] = df[column].astype(str)

# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.LNG, df.LAT)
)

# Convert the GeoDataFrame to GeoJSON
features = []
for _, row in df.iterrows():
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["LNG"], row["LAT"]],
        },
        "properties": {
            "tooltip": f"Customer Name: {row['Customer Name']}<br>Segment: {row['Segment']}<br>Country/Region: {row['Country/Region']}<br>City: {row['City']}<br>State/Province: {row['State/Province']}<br>Postal Code: {row['Postal Code']}<br>Region: {row['Region']}<br>Product ID: {row['Product ID']}<br>Category: {row['Category']}<br>Sub-Category: {row['Sub-Category']}<br>Product Name: {row['Product Name']}<br>Sales: {row['Sales']}<br>Quantity: {row['Quantity']}<br>Discount: {row['Discount']}<br>Profit: {row['Profit']}",
            "Category": row['Category'],
        }
    })

geojson_dict = {
    "type": "FeatureCollection",
    "features": features
}

# Load GeoJSON data setup borders for regions
with open('2024/week-28/path_to_regions_geojson_file.geojson', 'r') as f:
    regions_geojson = json.load(f)

# Function to style the GeoJSON features based on the 'Region' property
# Define color mapping for regions
region_colors = {
    'East': '#ff0000',
    'West': '#00ff00',
    'Central': '#0000ff',
    'South': '#ffff00',
    'Unknown': '#808080'  # Grey for unknown regions
}

# Create separate GeoJSON data for each region
region_geojsons = {region: {"type": "FeatureCollection", "features": []} for region in region_colors.keys()}

# Apply the style to each feature in the GeoJSON
for feature in regions_geojson['features']:
    state_province = feature['properties']['name']
    region = state_to_region.get(state_province, 'Unknown')
    feature['properties']['fillColor'] = region_colors.get(region, '#808080')
    region_geojsons[region]['features'].append(feature)

# Define color mapping for categories
category_colors = {
    'Office Supplies': 'white',
    'Technology': 'black',
    'Furniture': 'purple',
    'Unknown': 'gray'  # Color for unknown categories
}

#########################################
# Setup Layout
#########################################
dont_show = dmc.Stack(
            [
                dmc.TextInput(
                    placeholder="Filter Locations...",
                    style={"width": '95%', "margin-bottom": "9px"},
                    id="superstore_quick_filter_input",
                ),
                dmc.Group(
                    [
                        dmc.Select(
                            # label='Select a State',
                            placeholder="Select a State / Provence",
                            id="superstore_autocomplete_r_map",
                            value="Everything",
                            data=state_select_data,
                            style={
                                "width": '45%',
                                "marginBottom": 10,
                                "color": "red",
                            },
                        ),
                        dmc.Select(
                            placeholder="Category",
                            id="superstore_location_type",
                            value="everything",
                            data=[
                                {"label": "Everything", "value": "everything"},
                                {"label": "Office Supplies", "value": "Office Supplies"},
                                {"label": "Technology", "value": "Technology"},
                                {"label": "Furniture", "value": "Furniture"},
                            ],
                            style={
                                "width": '45%',
                                "marginBottom": 10,
                                "color": "red",
                            },
                        ),

                    ],
                    grow=False,
                    position="left",
                ),
                dag.AgGrid(
                    className="ag-theme-alpine-dark",
                    id="superstore_quick_filter_simple",
                    rowData=df.to_dict('records'),
                    columnDefs=[
            {"headerName": i, "field": i, "width": '100%'} for i in df.columns
        ] + [
            {
                "headerName": "Profit",
                "field": "Profit",
                "cellStyle": {
                    "styleConditions": [
                        {
                            "condition": "params.value > 0",
                            "style": {"backgroundColor": "rgba(0, 255, 0, 0.3)"}
                        },
                        {
                            "condition": "params.value < 0",
                            "style": {"backgroundColor": "rgba(255, 0, 0, 0.3)"}
                        },
                        {
                            "condition": "params.value == 0",
                            "style": {"backgroundColor": "rgba(255, 255, 255, 0.3)"}
                        }
                    ]
                },
                "width": '100%'
            }
        ],
                    defaultColDef={"filter": False, "editable": False},
                    dashGridOptions={
                        'suppressMenuHide': True,
                        "rowSelection": "single",
                        "animateRows": False,
                        "pagination": False,
                    },
                    style={},
                ),
            ], style={"display": "none"}
        )

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=["https://use.fontawesome.com/releases/v6.2.1/css/all.css",])

# Create the layout with a map and a table
app.layout = html.Div([
    dont_show,
    html.Div(
                    id="superstore_search_display",
                    style={
                        "position": "absolute",
                        "left": "60px",
                        "top": "8vh",
                        "zIndex": "1001",
                    },
                ),
    dmc.Grid(
        children=[
            dmc.Col(dl.Map(id="superstore_map", center=[39.8283, -98.5795], zoom=4, children=[
                dl.TileLayer(),
                dl.EasyButton(
                    icon="fa-search",
                    title="Search Map",
                    id="superstore_search_map_display_btn",
                    n_clicks=1,
                ),
                dl.GeoJSON(
                    data=geojson_dict,
                    id="superstore_locations_layer",
                    cluster=True,
                    zoomToBoundsOnClick=True,
                    superClusterOptions=dict(radius=40),
                    hideout=dict(
                        category_colors=category_colors,
                        circleOptions=dict(fillOpacity=1, stroke=False, radius=3),
                        min=0,
                    ),
                    clusterToLayer=cluster_to_layer,
                ),
                dl.GeoJSON(
                    data=region_geojsons['East'],
                    id="superstore_regions_layer_east",
                    hoverStyle=arrow_function(dict(weight=5, color='#777', dashArray='')),
                    style=dict(weight=2, fillColor=region_colors['East'], fillOpacity=0.7)
                ),
                dl.GeoJSON(
                    data=region_geojsons['West'],
                    id="superstore_regions_layer_west",
                    hoverStyle=arrow_function(dict(weight=5, color='#777', dashArray='')),
                    style=dict(weight=2, fillColor=region_colors['West'], fillOpacity=0.7)
                ),
                dl.GeoJSON(
                    data=region_geojsons['Central'],
                    id="superstore_regions_layer_central",
                    hoverStyle=arrow_function(dict(weight=5, color='#777', dashArray='')),
                    style=dict(weight=2, fillColor=region_colors['Central'], fillOpacity=0.7)
                ),
                dl.GeoJSON(
                    data=region_geojsons['South'],
                    id="superstore_regions_layer_south",
                    hoverStyle=arrow_function(dict(weight=5, color='#777', dashArray='')),
                    style=dict(weight=2, fillColor=region_colors['South'], fillOpacity=0.7)
                )
            ], style={'height': '100vh', 'width': '100%', 'margin': "auto", "display": "block"}), span=12),
            # dmc.Col(dcc.Graph(figure=fig_sankey, style={'height': '100vh', 'width': '100%', 'margin': "auto", "display": "block"}), span=6),
        ],
        gutter="xl",
    ),
])

#########################################
# Setup Callbacks
#########################################

@callback(
    Output("superstore_search_display", "children"),
    Input("superstore_search_map_display_btn", "n_clicks"),
)
def show_search_map(n_clicks):
    if n_clicks % 2 == 0:
        return dmc.Stack(
            [
                dmc.TextInput(
                    placeholder="Filter Locations...",
                    style={"width": '95%', "margin-bottom": "9px"},
                    id="superstore_quick_filter_input",
                ),
                dmc.Group(
                    [
                        dmc.Select(
                            # label='Select a State',
                            placeholder="Select a State / Provence",
                            id="superstore_autocomplete_r_map",
                            value="Everything",
                            data=state_select_data,
                            style={
                                "width": '45%',
                                "marginBottom": 10,
                                "color": "red",
                            },
                        ),
                        dmc.Select(
                            placeholder="Category",
                            id="superstore_location_type",
                            value="everything",
                            data=[
                                {"label": "Everything", "value": "everything"},
                                {"label": "Office Supplies", "value": "Office Supplies"},
                                {"label": "Technology", "value": "Technology"},
                                {"label": "Furniture", "value": "Furniture"},
                            ],
                            style={
                                "width": '45%',
                                "marginBottom": 10,
                                "color": "red",
                            },
                        ),

                    ],
                    grow=False,
                    position="left",
                ),
                dag.AgGrid(
                    className="ag-theme-alpine-dark",
                    id="superstore_quick_filter_simple",
                    rowData=df.to_dict('records'),
                    columnDefs=[
            {"headerName": i, "field": i, "width": '100%'} for i in df.columns
        ] + [
            {
                "headerName": "Profit",
                "field": "Profit",
                "cellStyle": {
                    "styleConditions": [
                        {
                            "condition": "params.value > 0",
                            "style": {"backgroundColor": "rgba(0, 255, 0, 0.3)"}
                        },
                        {
                            "condition": "params.value < 0",
                            "style": {"backgroundColor": "rgba(255, 0, 0, 0.3)"}
                        },
                        {
                            "condition": "params.value == 0",
                            "style": {"backgroundColor": "rgba(255, 255, 255, 0.3)"}
                        }
                    ]
                },
                "width": '100%'
            }
        ],
                    defaultColDef={"filter": False, "editable": False},
                    dashGridOptions={
                        'suppressMenuHide': True,
                        "rowSelection": "single",
                        "animateRows": False,
                        "pagination": False,
                    },
                    style={},
                ),
            ]
        )
    else:
        return []

@callback(
    Output("superstore_map", "viewport", allow_duplicate=True),
    Output("superstore_quick_filter_simple", "rowData", allow_duplicate=True),
    Input("superstore_autocomplete_r_map", "value"),
    prevent_initial_call=True,
)
def search_state_map(value):
    if value == "Everything":
        return dict(center=[39.8283, -98.5795], zoom=4, transition="flyTo"), df.to_dict("records")
    else:
        filtered_df = df[df['State/Province'] == value]
        if not filtered_df.empty:
            center_lat = filtered_df['LAT'].mean()
            center_lon = filtered_df['LNG'].mean()
            return dict(center=[center_lat, center_lon], zoom=6, transition="flyTo"), filtered_df.to_dict("records")
        else:
            return no_update, no_update

@callback(
    Output("superstore_quick_filter_simple", "dashGridOptions"),
    Output("superstore_locations_layer", "data", allow_duplicate=True),
    Output("superstore_quick_filter_simple", "rowData", allow_duplicate=True),
    Input("superstore_quick_filter_input", "value"),
    Input("superstore_location_type", "value"),
    Input('superstore_autocomplete_r_map', 'value'),
    prevent_initial_call=True,
)
def update_filter_and_locations_layer(filter_value, location_type, state):
    # Filter by state
    if state == "Everything":
        rowData = df
    else:
        rowData = df[df['State/Province'] == state]

    # Filter by category
    if location_type != "everything":
        rowData = rowData[rowData['Category'] == location_type]

    # Filter by name (assuming you want to filter by Customer Name)
    if filter_value:
        rowData = rowData[rowData['Customer Name'].str.contains(f'{filter_value}', case=False, na=False)]

    # Create GeoJSON features with tooltip
    features = []
    for _, row in rowData.iterrows():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["LNG"], row["LAT"]],
            },
            "properties": {
                "Category": row['Category'],
                "tooltip": f"Customer Name: {row['Customer Name']}<br>Segment: {row['Segment']}<br>Country/Region: {row['Country/Region']}<br>City: {row['City']}<br>State/Province: {row['State/Province']}<br>Postal Code: {row['Postal Code']}<br>Region: {row['Region']}<br>Product ID: {row['Product ID']}<br>Category: {row['Category']}<br>Sub-Category: {row['Sub-Category']}<br>Product Name: {row['Product Name']}<br>Sales: {row['Sales']}<br>Quantity: {row['Quantity']}<br>Discount: {row['Discount']}<br>Profit: {row['Profit']}"
            }
        })

    geojson_dict = {
        "type": "FeatureCollection",
        "features": features
    }

    # Update the quick filter
    newFilter = Patch()
    newFilter["quickFilterText"] = filter_value

    return newFilter, geojson_dict, rowData.to_dict("records")


@callback(
    Output("superstore_map", "viewport", allow_duplicate=True),
    Input("superstore_quick_filter_simple", "selectedRows"),
    prevent_initial_call=True,
)
def ag_grid_selection(selected_rows):
    if selected_rows:
        return dict(
            center=[selected_rows[0]['LAT'], selected_rows[0]['LNG']],
            zoom=10,
            transition="flyTo",
        )
    else:
        return no_update


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
"""

linguyen = """
# check out https://github.com/mckinsey/vizro for more info about Vizro
# and checkout https://vizro.readthedocs.io/en/stable/ for documentation

import pandas as pd
import vizro.models as vm
from charts import COLUMN_DEFS, scatter_with_quadrants
from vizro import Vizro
from vizro.actions import export_data, filter_interaction
from vizro.tables import dash_ag_grid

# TIDY DATA
df = pd.read_excel("Sample - Superstore.xls")
df["Category / Sub-Category"] = df["Category"] + " / " + df["Sub-Category"]
df = df.groupby(["Category / Sub-Category", "Product Name"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
df["Profit Margin"] = df["Profit"] / df["Sales"]
df["Profit Absolute"] = abs(df["Profit"])  # For size in px.scatter (cannot be negative)


# DEFINE PAGE AND DASHBOARD
page = vm.Page(
    title="Week 28 - Sales vs. Profit 📈",
    id="page-id",
    layout=vm.Layout(grid=[[0, 1]] * 6 + [[2, -1]]),
    components=[
        vm.Graph(
            id="scatter",
            figure=scatter_with_quadrants(data_frame=df, x="Sales", y="Profit", custom_data=["Product Name", "Profit Margin"]),
            actions=[vm.Action(function=filter_interaction(targets=["table"]))],
        ),
        vm.AgGrid(id="table", figure=dash_ag_grid(df, columnDefs=COLUMN_DEFS)),
        vm.Button(
            text="Export data",
            actions=[
                vm.Action(function=export_data()),
            ],
        ),
    ],
    controls=[
        vm.Filter(column="Category / Sub-Category", selector=vm.Dropdown(multi=False, value="Technology / Phones")),
        vm.Parameter(
            targets=["scatter.x_ref_quantile"],
            selector=vm.Slider(min=0, max=1, step=0.2, value=0.8, title="X-reference line (quantile)"),
        ),
        vm.Parameter(
            targets=["scatter.y_ref_quantile"],
            selector=vm.Slider(min=0, max=1, step=0.2, value=0.2, title="Y-reference line (quantile)"),
        ),
    ],
)

dashboard = vm.Dashboard(pages=[page], title="Figure Friday", theme="vizro_light")
Vizro(assets_folder=".").build(dashboard).run()
"""

component = html.Div(
    [
        dmc.AvatarGroup(
            children=[
                dmc.Tooltip(
                    label="li.nguyen",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(
                    src="https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/li.nguyen/288/26333_2.png",
                    radius="xl",
                )]
                ),
                dmc.Tooltip(
                    label="chenyulue",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(
                    src="https://avatars.discourse-cdn.com/v4/letter/c/73ab20/288.png",
                    radius="xl",
                )]
                ),
                dmc.Tooltip(
                    label="AnnMarieW",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(
                    src="https://avatars.discourse-cdn.com/v4/letter/a/ec9cab/288.png",
                    radius="xl",
                )]
                ),
                dmc.Tooltip(
                    label="DenysC",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(
                    src="https://avatars.discourse-cdn.com/v4/letter/d/a587f6/288.png",
                    radius="xl",
                )]
                ),
                dmc.Tooltip(
                    label="PipInstallPython",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(src="https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/pipinstallpython/288/28458_2.png",
                                         radius="xl")]
                ),
                dmc.Tooltip(
                    label="jens",
                    position="top",
                    offset=3,
                    children=[dmc.Avatar(src="https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/jens/288/28502_2.png",
                                         radius="xl")]
                ),
            ],
        ),
        dmc.Select(
            label="Select Users Submission",
            placeholder="Select one",
            id="week_28_submissions",
            value="PipInstallPython",
            data=[
                {"value": "li.nguyen", "label": "li.nguyen"},
                {"value": "chenyulue", "label": "chenyulue"},
                {"value": "AnnMarieW", "label": "AnnMarieW"},
                {"value": "DenysC", "label": "DenysC"},
                {"value": "PipInstallPython", "label": "PipInstallPython"},
                {"value": "jens", "label": "jens"},
            ],
            w=200,
            mb=10,
        ),
        html.Div(id="week_28_preview"),
        html.Div(
        DashAceEditor(
                                id="week_28_code",
                                value=example_code,
                                theme="monokai",
                                mode="python",
                                tabSize=2,
                                enableBasicAutocompletion=True,
                                enableLiveAutocompletion=True,
                                autocompleter="/autocompleter?prefix=",
                                placeholder="Python code ...",
                                style={"height": "500px", "width": "auto"},
                            ))
    ]
)

@callback(
Output("week_28_preview", "children"),
    Output("week_28_code", "value"),
    Input("week_28_submissions", "value"),
)
def load_submission(value):
    if value == "PipInstallPython":
        return html.Iframe(src="https://dash.geomapindex.com/figure_friday_week_1", style={"width": "100%", "height": "500px"}), pipinstallpython
    elif value == "li.nguyen":
        return html.Img(src="https://global.discourse-cdn.com/business7/uploads/plot/original/3X/7/6/76b51eda9fe1159c1b5bcb5aad6cfff86f1a8f40.gif", style={"height": "500px", "width": "100%"}), linguyen
    else:
        return example_code
