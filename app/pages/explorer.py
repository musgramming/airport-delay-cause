from dash import html, dcc, callback, Input, Output, State, no_update, register_page, dash_table, callback_context
import dash_bootstrap_components as dbc
import polars as pl 
import plotly.express as px

from output import DETAIL, MAIN_DF, AIRPORT_TABLE, CARRIER_TABLE, CARRIER_AIRPORT_MAP

register_page(__name__, path="/explorer")





left_layout = dbc.Card([
    dbc.CardHeader(html.H4("🔍 Bộ lọc thông minh", className="mb-0")),
    dbc.CardBody([
        html.Div([
            html.Label("1. Hãng hàng không:", className="fw-bold"),
            dcc.Dropdown(
                id="exp-carrier-sel",
                options=[{"label": r["carrier_name"], "value": r["carrier"]} 
                         for r in CARRIER_TABLE.collect().to_dicts()],
                multi=True,
                placeholder="Tất cả hãng..."
            ),
        ], className="mb-3"),

        html.Div([
            html.Label("2. Sân bay:", className="fw-bold"),
            dcc.Dropdown(
                id="exp-airport-sel",
                options=[{"label": f"{r['airport_name']} ({r['airport']})", "value": r["airport"]} 
                         for r in AIRPORT_TABLE.collect().to_dicts()],
                multi=True,
                placeholder="Tất cả sân bay..."
            ),
        ], className="mb-3"),

        html.Div([
            html.Label("3. Bạn muốn soi gì?", className="fw-bold"),
            dbc.RadioItems(
                id="exp-question-type",
                options=[
                    {"label": "Số lượng (Count)", "value": "count"},
                    {"label": "Thời gian trễ (Delay)", "value": "delay"},
                ],
                value="count",
                inline=True,
            ),
        ], className="mb-3"),

        html.Div([
            html.Label("4. Thông số cụ thể:", className="fw-bold"),
            dcc.Dropdown(id="exp-col-sel"),
        ], className="mb-4"),

        dbc.Button("Khám phá ngay", id="exp-run-btn", color="primary", className="w-100")
    ])
], className="shadow-sm")



# --- PHẦN HIỂN THỊ BÊN PHẢI ---
right_layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label="📊 Biểu đồ Facet", tab_id="tab-chart"),
        dbc.Tab(label="📋 Bảng dữ liệu", tab_id="tab-table"),
    ], id="exp-tabs", active_tab="tab-chart"),
    
    html.Div(id="exp-content", className="mt-4")
])

layout = dbc.Container([
    dbc.Row([
        dbc.Col(left_layout, md=4, lg=3),
        dbc.Col(right_layout, md=8, lg=9),
    ])
], fluid=True, className="py-4")





# --- CALLBACKS ---

@callback(
    Output("exp-carrier-sel", "options"),
    Output("exp-airport-sel", "options"),
    Input("exp-carrier-sel", "value"),
    Input("exp-airport-sel", "value"),
)
def sync_dropdowns(selected_carriers, selected_airports):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    mapping = CARRIER_AIRPORT_MAP.with_columns([
        pl.col("carrier").cast(pl.Utf8),
        pl.col("airport").cast(pl.Utf8)
    ])

    if trigger_id == "exp-carrier-sel" and selected_carriers:
        valid_map = mapping.filter(pl.col("carrier").is_in(selected_carriers))
    elif trigger_id == "exp-airport-sel" and selected_airports:
        valid_map = mapping.filter(pl.col("airport").is_in(selected_airports))
    else:
        valid_map = mapping

    res_df = valid_map.collect()
    valid_c_list = res_df.get_column("carrier").unique().to_list()
    valid_a_list = res_df.get_column("airport").unique().to_list()

    carrier_options = [
        {"label": r["carrier_name"], "value": r["carrier"]}
        for r in CARRIER_TABLE.filter(pl.col("carrier").is_in(valid_c_list)).collect().to_dicts()
    ]

    airport_options = [
        {"label": f"{r['airport_name']} ({r['airport']})", "value": r["airport"]}
        for r in AIRPORT_TABLE.filter(pl.col("airport").is_in(valid_a_list)).collect().to_dicts()
    ]

    return carrier_options, airport_options




@callback(
    Output("exp-col-sel", "options"),
    Output("exp-col-sel", "value"),
    Input("exp-question-type", "value")
)
def update_column_options(q_type):
    filtered_df = DETAIL.filter(pl.col("group") == q_type).collect()
    options = [{"label": row["details"], "value": row["name"]} for row in filtered_df.to_dicts()]
    return options, options[0]["value"] if options else None






@callback(
    Output("exp-content", "children"),
    Input("exp-run-btn", "n_clicks"),
    State("exp-tabs", "active_tab"),
    State("exp-carrier-sel", "value"),
    State("exp-airport-sel", "value"),
    State("exp-col-sel", "value"),
    prevent_initial_call=True
)
def process_explorer_data(n_clicks, active_tab, carriers, airports, selected_col):
    if not n_clicks or not selected_col:
        return no_update

    try:
        lf = MAIN_DF.with_columns([
            pl.col("carrier").cast(pl.Utf8),
            pl.col("airport").cast(pl.Utf8)
        ])

        if carriers:
            lf = lf.filter(pl.col("carrier").is_in(carriers))
        if airports:
            lf = lf.filter(pl.col("airport").is_in(airports))

        query = (
            lf.group_by(["flight_date", "carrier", "airport"])
            .agg(pl.col(selected_col).fill_null(0).sum().alias("y_value"))
            .sort("flight_date")
        )

        df_final = query.collect().to_pandas()
        
        if df_final.empty:
            return dbc.Alert("⚠️ Không có dữ liệu phù hợp. Hãy thử bớt bộ lọc!", color="warning")

        df_c = CARRIER_TABLE.with_columns(pl.col("carrier").cast(pl.Utf8)).collect().to_pandas()
        df_a = AIRPORT_TABLE.with_columns(pl.col("airport").cast(pl.Utf8)).collect().to_pandas()
        
        df_final = df_final.merge(df_c, on="carrier", how="left").merge(df_a, on="airport", how="left")
        
        df_final["facet_label"] = (
            df_final["carrier_name"] + " | " + 
            df_final["airport_name"].str.slice(0, 30) + "..."
        )

        detail_df = DETAIL.collect()
        display_label = detail_df.filter(pl.col("name") == selected_col)["details"][0]

        if active_tab == "tab-chart":
            num_plots = df_final["facet_label"].nunique()
            wrap_val = max(1, len(carriers)) if carriers else 2
            rows = (num_plots + wrap_val - 1) // wrap_val
            
            dynamic_height = max(500, rows * 380) 

            fig = px.line(
                df_final, 
                x="flight_date", 
                y="y_value", 
                color="carrier_name",
                facet_col="facet_label", 
                facet_col_wrap=wrap_val,
                facet_row_spacing=0.15, # Tăng khoảng cách hàng lên 15%
                facet_col_spacing=0.07,
                template="plotly_dark",
                labels={"y_value": "Giá trị", "flight_date": "Ngày", "carrier_name": "Hãng"},
                title=f"Phân tích hệ thống: {display_label}"
            )

            fig.update_annotations(patch={
                "textangle": 0, 
                "yshift": 35, 
                "font": {"size": 11, "color": "#00d4ff"} 
            })
            
            fig.update_layout(
                margin=dict(t=120, b=100, l=60, r=40),
                hovermode="x unified",
                showlegend=True,
                legend=dict(
                    orientation="v",        
                    yanchor="top",          
                    y=-0.15,                
                    xanchor="center", 
                    x=0.5
                )
            )

            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

            fig.update_yaxes(matches='y', showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')

            return dcc.Graph(figure=fig, style={"height": f"{dynamic_height}px"})
        
        return dash_table.DataTable(
            data=df_final.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df_final.columns if i != "facet_label"],
            page_size=12,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#1a1a1a', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={'backgroundColor': '#2d2d2d', 'color': 'white'}
        )

    except Exception as e:
        return dbc.Alert(f"Đã xảy ra lỗi: {str(e)}", color="danger")