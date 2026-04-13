from dash import html, page_container
import dash_bootstrap_components as dbc

layout = html.Div([
    # Dùng Navbar thay vì Header thuần cho chuyên nghiệp
    dbc.Navbar(
        dbc.Container(
            dbc.NavbarBrand("AIRPORT DASHBOARD", href="#", className="mx-auto h1 mb-0"),
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-4" # Thêm chút margin bottom cho thoáng
    ),

    dbc.Container([
        # Khu vực hiển thị nội dung các trang con
        page_container 
    ], className="mt-4"),

    # Footer chuyên nghiệp hơn
    html.Footer(
        dbc.Container(
            [
                html.Hr(),
                html.P([
                    "Data source: ", 
                    html.A("Kaggle", href="https://www.kaggle.com/datasets/youssefayman22/airline-delay-cause-csv", target="_blank", className="text-decoration-none"),
                    html.Br(),
                    "Built by Mus"
                ], className="text-muted")
            ]
        ),
        className="footer mt-auto py-3 text-center"
    )
], style={"display": "flex", "flex-direction": "column", "min-height": "100vh"})
