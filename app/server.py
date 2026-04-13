import sys
from pathlib import Path
from flask import Flask 
from dash import Dash
import dash_bootstrap_components as dbc
# Import cái layout khung mà bạn vừa gửi
from app.layout import layout 

# 1. Ninja Trick: Đảm bảo Python thấy root để import 'output' hay các module khác mượt mà
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# 2. Xác định đường dẫn tuyệt đối cho folder pages
# Vì server.py nằm trong app/, nên folder pages cũng nằm ngay đây
pages_folder = Path(__file__).parent / "pages"

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    use_pages=True,
    # Dùng .as_posix() để tránh lỗi dấu xuôi/ngược trên Windows
    pages_folder=pages_folder.as_posix(), 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Gán cái layout khung (có page_container) vào app
app.layout = layout

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
