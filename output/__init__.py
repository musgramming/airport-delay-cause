import polars as pl
from pathlib import Path

# Xác định thư mục chứa chính file __init__.py này (chính là thư mục output)
_HERE = Path(__file__).parent

# Kết nối đường dẫn đến các file dữ liệu
AIRPORT_TABLE = pl.scan_parquet(_HERE / "airport.parquet")
CARRIER_TABLE = pl.scan_parquet(_HERE / "carrier.parquet")
MAIN_DF = pl.scan_parquet(_HERE / "main_df.parquet")

# File CSV gây lỗi đây, giờ nó sẽ luôn tìm đúng địa chỉ
DETAIL = pl.scan_csv(_HERE / "detail.csv")

CARRIER_AIRPORT_MAP = pl.scan_parquet(_HERE / "carrier_airport_map.parquet")