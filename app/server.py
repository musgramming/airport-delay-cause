import sys
import os
from pathlib import Path
from flask import Flask 
from dash import Dash
import dash_bootstrap_components as dbc

from app.layout import layout 

root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

pages_folder = Path(__file__).parent / "pages"

app = Dash(
    __name__,
    use_pages=True,
    pages_folder=pages_folder.as_posix(), 
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

server = app.server 

app.layout = layout

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        debug=True
    )
