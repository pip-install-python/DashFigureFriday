import dash
from dash import Dash, _dash_renderer
import json
from flask import jsonify
from components.appshell import create_appshell

_dash_renderer._set_react_version("18.2.0")

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    # "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
    'https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.css'
]

scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/ru.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/fr.min.js",
    "https://unpkg.com/hotkeys-js/dist/hotkeys.min.js",
]



app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    external_scripts=scripts,
    external_stylesheets=stylesheets,
    update_title=None,
    prevent_initial_callbacks=True,
)


app.layout = create_appshell(dash.page_registry.values())

server = app.server


if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port='8550')
