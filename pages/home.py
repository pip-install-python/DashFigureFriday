from pathlib import Path
import dash
import frontmatter
import dash_mantine_components as dmc
from dash import dcc, register_page, callback, Output, html, Input, State, callback_context
import full_calendar_component as fcc
from datetime import datetime, date, timedelta
from lib.constants import PAGE_TITLE_PREFIX
from dash.exceptions import PreventUpdate
import dash_quill

quill_mods = [
    [{"header": "1"}, {"header": "2"}, {"font": []}],
    [{"size": []}],
    ["bold", "italic", "underline", "strike", "blockquote"],
    [{"list": "ordered"}, {"list": "bullet"}, {"indent": "-1"}, {"indent": "+1"}],
    ["link", "image"],
]

# Get today's date
today = datetime.now()

# Format the date
formatted_date = today.strftime("%Y-%m-%d")
register_page(
    __name__,
    "/",
    title=PAGE_TITLE_PREFIX + "Home",
)

directory = "docs"

# read all markdown files
md_file = Path("pages") / "home.md"

metadata, content = frontmatter.parse(md_file.read_text())


# directives = [Admonition(), BlockExec(), Divider(), Image(), Kwargs(), SC(), TOC()]
# parse = create_parser(directives)

# Setup the calendar events
today = datetime.now()

# Format the date
formatted_date = today.strftime("%Y-%m-%d")

week_28 = """
Hey Everyone,
We’re excited to announce the first data set of the Figure Friday initiative 9. Every Friday Plotly will release a data set and a sample figure. The community will have one week to enhance that figure, build your own Plotly figure or create a Dash app.

This week’s data set comes from Workout Wednesday and it’s a sample superstore’s sales and profit 32.

"""


events = [
    {
        "title": "Week 28",
        "start": f"2024-07-12",
        "end": f"2024-07-19",
        "className": "bg-gradient-success",
        "context": "Pip Install FullCalendar",
    },
    {
        "title": "Week 29",
        "start": f"2024-07-19",
        "end": f"2024-07-26",
        "className": "bg-gradient-info",
        "context": "Meeting with the boss",
    },
    {
        "title": "Week 30",
        "start": f"2024-07-26",
        "end": f"2024-08-02",
        "className": "bg-gradient-warning",
        "context": "Happy Hour",
    },
    {
        "title": "Week 31",
        "start": f"2024-08-02",
        "end": f"2024-08-09",
        "className": "bg-gradient-danger",
        "context": "Dinner",
    },
]

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=30,
            children=dcc.Markdown(content)
        ),
        html.Div(
            [
                fcc.FullCalendarComponent(
                    id="calendar",  # Unique ID for the component
                    initialView="dayGridMonth",  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
                    # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
                    headerToolbar={
                        "left": "prev,next today",
                        "center": "",
                        "right": "listWeek,timeGridDay,timeGridWeek,dayGridMonth",
                    },  # Calendar header
                    initialDate=f"{formatted_date}",  # Start date for calendar
                    editable=True,  # Allow events to be edited
                    selectable=True,  # Allow dates to be selected
                    events=events,
                    nowIndicator=True,  # Show current time indicator
                    navLinks=True,  # Allow navigation to other dates
                ),
                dmc.MantineProvider(
                    theme={"colorScheme": "dark"},
                    children=[
                        dmc.Modal(
                            id="modal",
                            size="xl",
                            title="Event Details",
                            zIndex=10000,
                            centered=True,
                            children=[
                                html.Div(id="modal_event_display_context"),
                                dmc.Space(h=20),
                                dmc.Group(
                                    [
                                        dmc.Button(
                                            "Close",
                                            color="red",
                                            variant="outline",
                                            id="modal-close-button",
                                        ),
                                    ],
                                    align="right",
                                ),
                            ],
                        )
                    ],
                ),
                dmc.MantineProvider(
                    theme={"colorScheme": "dark"},
                    children=[
                        dmc.Modal(
                            id="add_modal",
                            title="New Event",
                            size="xl",
                            centered=True,
                            children=[
                                dmc.Grid(
                                    children=[
                                        dmc.GridCol(
                                            html.Div(
                                                dmc.DatePicker(
                                                    id="start_date",
                                                    label="Start Date",
                                                    value=datetime.now().date(),
                                                    styles={"width": "100%"},
                                                    disabled=True,
                                                ),
                                                style={"width": "100%"},
                                            ),
                                            span=6,
                                        ),
                                        dmc.GridCol(
                                            html.Div(
                                                dmc.TimeInput(
                                                    label="Start Time",
                                                    withSeconds=True,
                                                    value=datetime.now(),
                                                    # format="12",
                                                    id="start_time",
                                                ),
                                                style={"width": "100%"},
                                            ),
                                            span=6,
                                        ),
                                    ],
                                    gutter="xl",
                                ),
                                dmc.Grid(
                                    children=[
                                        dmc.GridCol(
                                            html.Div(
                                                dmc.DatePicker(
                                                    id="end_date",
                                                    label="End Date",
                                                    value=datetime.now().date(),
                                                    styles={"width": "100%"},
                                                ),
                                                style={"width": "100%"},
                                            ),
                                            span=6,
                                        ),
                                        dmc.GridCol(
                                            html.Div(
                                                dmc.TimeInput(
                                                    label="End Time",
                                                    withSeconds=True,
                                                    value=datetime.now(),
                                                    # format="12",
                                                    id="end_time",
                                                ),
                                                style={"width": "100%"},
                                            ),
                                            span=6,
                                        ),
                                    ],
                                    gutter="xl",
                                ),
                                dmc.Grid(
                                    children=[
                                        dmc.GridCol(
                                            span=6,
                                            children=[
                                                dmc.TextInput(
                                                    label="Event Title:",
                                                    style={"width": "100%"},
                                                    id="event_name_input",
                                                    required=True,
                                                )
                                            ],
                                        ),
                                        dmc.GridCol(
                                            span=6,
                                            children=[
                                                dmc.Select(
                                                    label="Select event color",
                                                    placeholder="Select one",
                                                    id="event_color_select",
                                                    value="ng",
                                                    data=[
                                                        {
                                                            "value": "bg-gradient-primary",
                                                            "label": "bg-gradient-primary",
                                                        },
                                                        {
                                                            "value": "bg-gradient-secondary",
                                                            "label": "bg-gradient-secondary",
                                                        },
                                                        {
                                                            "value": "bg-gradient-success",
                                                            "label": "bg-gradient-success",
                                                        },
                                                        {
                                                            "value": "bg-gradient-info",
                                                            "label": "bg-gradient-info",
                                                        },
                                                        {
                                                            "value": "bg-gradient-warning",
                                                            "label": "bg-gradient-warning",
                                                        },
                                                        {
                                                            "value": "bg-gradient-danger",
                                                            "label": "bg-gradient-danger",
                                                        },
                                                        {
                                                            "value": "bg-gradient-light",
                                                            "label": "bg-gradient-light",
                                                        },
                                                        {
                                                            "value": "bg-gradient-dark",
                                                            "label": "bg-gradient-dark",
                                                        },
                                                        {
                                                            "value": "bg-gradient-white",
                                                            "label": "bg-gradient-white",
                                                        },
                                                    ],
                                                    style={"width": "100%", "marginBottom": 10},
                                                    required=True,
                                                )
                                            ],
                                        ),
                                    ]
                                ),
                                dash_quill.Quill(
                                    id="rich_text_input",
                                    modules={
                                        "toolbar": quill_mods,
                                        "clipboard": {
                                            "matchVisual": False,
                                        },
                                    },
                                ),
                                dmc.Accordion(
                                    children=[
                                        dmc.AccordionItem(
                                            [
                                                dmc.AccordionControl("Raw HTML"),
                                                dmc.AccordionPanel(
                                                    html.Div(
                                                        id="rich_text_output",
                                                        style={
                                                            "height": "300px",
                                                            "overflowY": "scroll",
                                                        },
                                                    )
                                                ),
                                            ],
                                            value="raw_html",
                                        ),
                                    ],
                                ),
                                dmc.Space(h=20),
                                dmc.Group(
                                    [
                                        dmc.Button(
                                            "Submit",
                                            id="modal_submit_new_event_button",
                                            color="green",
                                        ),
                                        dmc.Button(
                                            "Close",
                                            color="red",
                                            variant="outline",
                                            id="modal_close_new_event_button",
                                        ),
                                    ],
                                    align="right",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ]
)

@callback(
    Output("modal", "opened"),
    Output("modal", "title"),
    Output("modal_event_display_context", "children"),
    Input("modal-close-button", "n_clicks"),
    Input("calendar", "clickedEvent"),
    State("modal", "opened"),
    prevent_initial_call=True,  # Set this to True
)
def open_event_modal(n, clickedEvent, opened):

    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "calendar" and clickedEvent is not None:
        event_title = clickedEvent["title"]
        event_context = clickedEvent["extendedProps"]["context"]
        return (
            True,
            event_title,
            html.Div([
                dmc.Space(h=10),
                dash_quill.Quill(
                    id="input3",
                    value=f"{event_context}",
                    modules={
                        "toolbar": False,
                        "clipboard": {
                            "matchVisual": False,
                        },
                    },
                )
                ],
                style={"width": "100%", "overflowY": "auto"},
            ),
        )
    elif button_id == "modal-close-button" and n is not None:
        return False, dash.no_update, dash.no_update

    return opened, dash.no_update


@callback(
    Output("add_modal", "opened"),
    Output("start_date", "value"),
    Output("end_date", "value"),
    Output("start_time", "value"),
    Output("end_time", "value"),
    Input("calendar", "dateClicked"),
    Input("modal_close_new_event_button", "n_clicks"),
    State("add_modal", "opened"),
)
def open_add_modal(dateClicked, close_clicks, opened):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "calendar" and dateClicked is not None:
        try:
            start_time = datetime.strptime(dateClicked, "%Y-%m-%dT%H:%M:%S%z").time()
            start_date_obj = datetime.strptime(dateClicked, "%Y-%m-%dT%H:%M:%S%z")
            start_date = start_date_obj.strftime("%Y-%m-%d")
            end_date = start_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            start_time = datetime.now().time()
            start_date_obj = datetime.strptime(dateClicked, "%Y-%m-%d")
            start_date = start_date_obj.strftime("%Y-%m-%d")
            end_date = start_date_obj.strftime("%Y-%m-%d")
        end_time = datetime.combine(date.today(), start_time) + timedelta(hours=1)
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
        return True, start_date, end_date, start_time_str, end_time_str

    elif button_id == "modal_close_new_event_button" and close_clicks is not None:
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    return opened, dash.no_update, dash.no_update, dash.no_update, dash.no_update


@callback(
    Output("calendar", "events"),
    Output("add_modal", "opened", allow_duplicate=True),
    Output("event_name_input", "value"),
    Output("event_color_select", "value"),
    Output("rich_text_input", "value"),
    Input("modal_submit_new_event_button", "n_clicks"),
    State("start_date", "value"),
    State("start_time", "value"),
    State("end_date", "value"),
    State("end_time", "value"),
    State("event_name_input", "value"),
    State("event_color_select", "value"),
    State("rich_text_output", "children"),
    State("calendar", "events"),
    prevent_initial_call=True,  # Set this to True
)
def add_new_event(
    n,
    start_date,
    start_time,
    end_date,
    end_time,
    event_name,
    event_color,
    event_context,
    current_events,
):
    if n is None:
        raise PreventUpdate

    start_time_obj = datetime.strptime(start_time, "%H:%M:%S")
    end_time_obj = datetime.strptime(end_time, "%H:%M:%S")

    start_time_str = start_time_obj.strftime("%H:%M:%S")
    end_time_str = end_time_obj.strftime("%H:%M:%S")

    start_date = f"{start_date}T{start_time_str}"
    end_date = f"{end_date}T{end_time_str}"

    new_event = {
        "title": event_name,
        "start": start_date,
        "end": end_date,
        "className": event_color,
        "context": event_context,
    }

    return current_events + [new_event], False, "", "bg-gradient-primary", ""


@callback(
    Output("rich_text_output", "children"),
    [Input("rich_text_input", "value")],
    [State("rich_text_input", "charCount")],
)
def display_output(value, charCount):
    return value

