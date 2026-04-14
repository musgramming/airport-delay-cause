import polars as pl

import polars as pl

def get_dynamic_options(metadata_df: pl.LazyFrame):
    options = []
    df = metadata_df.collect()
    
    group_order = ["count", "delay"]
    group_labels = {
        "count": "--- PHẦN TRĂM & SỐ LƯỢNG ---", 
        "delay": "--- TỔNG THỜI GIAN (PHÚT) ---"
    }
    
    for group in group_order:
        options.append({"label": group_labels[group], "value": "header", "disabled": True})
        
        subset = df.filter(pl.col("group") == group)
        for row in subset.iter_rows(named=True):
            options.append({
                "label": f"   {row['details']}",
                "value": row['name']
            })
            
    return options
