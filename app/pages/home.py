from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/')

welcome_banner = dbc.Container([
    html.Div([
        html.H1("AIRLINE DELAY ANALYSIS SYSTEM", className="display-3 fw-bold text-primary"),
        html.P(
            "Hệ thống phân tích và chẩn đoán dữ liệu hàng không vận hành trên nền tảng Polars & Dash.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P("Khám phá xu hướng, lưu lượng và nguyên nhân gây chậm trễ từ hơn 20 năm dữ liệu lịch sử."),
    ], className="py-5")
], fluid=True, className="bg-light mb-4 shadow-sm")



nav_cards = dbc.Row([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("📊 Market Analytics", className="card-title"),
                html.P("So sánh hiệu suất giữa các hãng hàng không và sân bay. Phân tích các chỉ số KPI trọng yếu."),
                dbc.Button("Khám phá ngay", href="/analytics", color="primary", outline=True)
            ])
        ], className="h-100 shadow-sm hover-shadow"), # Thêm chút hiệu ứng shadow
        width=12, md=6, lg=4
    ),
    
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("🔍 Data Explorer", className="card-title"),
                html.P("Tra cứu chi tiết từng mốc thời gian. Tìm hiểu về các nhóm lỗi: Weather, NAS, Carrier..."),
                dbc.Button("Xem chi tiết", href="/explorer", color="info", outline=True)
            ])
        ], className="h-100 shadow-sm"),
        width=12, md=6, lg=4
    ),

    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("🛠️ System Tech Stack", className="card-title"),
                html.P("Backend: Polars (LazyFrame) | Frontend: Dash Plotly | Arch: Multi-page App."),
                dbc.Button("Project Info", href="https://github.com/musgramming/airport-delay-cause", color="dark", outline=True)
            ])
        ], className="h-100 shadow-sm"),
        width=12, md=6, lg=4
    ),
], className="g-4")

layout = html.Div([
    welcome_banner,
    dbc.Container([
        nav_cards,
        html.Div(style={"height": "100px"})
    ])
])