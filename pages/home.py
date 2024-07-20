from pathlib import Path

import frontmatter
import dash_mantine_components as dmc
from dash import dcc, register_page
from dash import html
import full_calendar_component as fcc
from datetime import datetime, date, timedelta
from lib.constants import PAGE_TITLE_PREFIX

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
        fcc.FullCalendarComponent(
            id="view-calendar-figure-friday",  # Unique ID for the component
            initialView="dayGridMonth",  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    ]
)
