from dash import html, dcc, callback, Input, Output, State, no_update, register_page
import dash_bootstrap_components as dbc
import polars as pl 
import plotly.express as px

from output import DETAIL, MAIN_DF, AIRPORT_TABLE, CARRIER_TABLE
from app.utils.columns import get_dynamic_options

register_page(
    __name__, 
    path = "/analytics"
)

first_layout = html.Div([
    dbc.Card([
        dbc.CardHeader(html.H2("1. Overview")),

        dbc.CardBody([
            html.Div([
                html.Label("Group by?"),
                dbc.RadioItems(
                    id="group-by-selector",
                    options = [
                        {"label" : "By Carrier", "value" : "carrier"},
                        {"label" : "By Airport", "value" : "airport"},
                    ],
                    value = "carrier"
                )
            ]),

            html.Br(),
            
            html.Div([
                html.Label("And col?", style={"fontWeight": "bold", "marginBottom": "10px"}),
                dbc.Select(
                    id="column-selector",
                    options=get_dynamic_options(DETAIL),
                    value="arr_del15", 
                    persistence=True,
                    persistence_type="session"
                ),
                dbc.FormText("Chọn thông số cụ thể bạn muốn phân tích trên biểu đồ.")
            ], style={"marginTop": "20px"}),

            html.Br(),

            html.Div([
                dbc.Button(
                    "Vẽ biểu đồ", 
                    id="draw-button", 
                    color="primary",
                    className="mt-3",
                    n_clicks=0
                )
            ], style={"textAlign": "right"})
        ])
    ])
])


second_layout = dbc.Container([
    dbc.Card([
        dbc.Spinner(
            dcc.Graph(id="overview-graph"),
            type="border"
        )
    ])
])



layout = dbc.Container([
    dbc.Row([
        dbc.Col(first_layout, width=3),
        dbc.Col(second_layout, width=9)    
    ])
], fluid=True, className="py-3")


@callback(
    Output("overview-graph", "figure"),
    Input("draw-button", "n_clicks"),
    State("group-by-selector", "value"),
    State("column-selector", "value"),
    prevent_initial_callback=True
)
def update_overview_graph(n_clicks, group_by, selected_col):
    if n_clicks == 0 or not group_by or not selected_col:
        return no_update

    try:
        lookup_table = CARRIER_TABLE if group_by == "carrier" else AIRPORT_TABLE
        
        query = (
            MAIN_DF
            .with_columns(pl.col(group_by).cast(pl.Utf8)) 
            .group_by(group_by)
            .agg(pl.col(selected_col).sum().alias("total_value"))
            .join(
                lookup_table.with_columns(pl.col(group_by).cast(pl.Utf8)),
                on=group_by,
                how="inner"
            )
            .sort("total_value", descending=True)
            .head(15)
        )

        df_plot = query.collect().to_pandas()
        
        if df_plot.empty:
            print("⚠️ CẢNH BÁO: Kết quả rỗng! Có thể do lệch mã định danh giữa 2 bảng.")
            return no_update

        display_name = f"{group_by}_name"

        fig = px.bar(
            df_plot,
            x="total_value",
            y=display_name,
            orientation='h',
            title=f"Top 15 {group_by.upper()} theo {selected_col.replace('_', ' ').title()}",
            color="total_value",
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Tổng số lượng",
            yaxis_title=group_by.capitalize(),
            margin=dict(l=20, r=20, t=60, b=20)
        )

        return fig

    except Exception as e:
        print(f"❌ Lỗi Callback: {str(e)}")
        return no_update
