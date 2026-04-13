import polars as pl

import polars as pl

def get_dynamic_options(metadata_df: pl.LazyFrame):
    options = []
    # 1. Chuyển từ Lazy sang Eager để có thể lấy dữ liệu ra xử lý vòng lặp
    df = metadata_df.collect()
    
    group_order = ["count", "delay"]
    group_labels = {
        "count": "--- PHẦN TRĂM & SỐ LƯỢNG ---", 
        "delay": "--- TỔNG THỜI GIAN (PHÚT) ---"
    }
    
    for group in group_order:
        # Thêm header nhóm
        options.append({"label": group_labels[group], "value": "header", "disabled": True})
        
        # 2. Dùng filter của Polars thay vì subscripting kiểu Pandas
        subset = df.filter(pl.col("group") == group)
        
        # 3. Polars không có iterrows(), ta dùng iter_rows(named=True) cực kỳ tiện
        for row in subset.iter_rows(named=True):
            options.append({
                "label": f"   {row['details']}",
                "value": row['name']
            })
            
    return options