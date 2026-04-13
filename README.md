# ✈️ Flight Data Explorer - IS Graduation Project 2025

Phân đoạn "Khám phá dữ liệu" (Explorer) thuộc hệ thống phân tích dữ liệu hàng không Quốc gia năm 2025. Ứng dụng được xây dựng trên nền tảng Dash & Polars, tối ưu hóa cho việc truy vấn ma trận và trực quan hóa xu hướng trễ chuyến.

## 📊 Data Source
Dữ liệu được sử dụng trong dự án là bộ dữ liệu công khai về nguyên nhân chậm chuyến bay:
- **Tên Dataset:** Airline Delay Cause
- **Nguồn:** [Kaggle - Youssef Ayman](https://www.kaggle.com/datasets/youssefayman22/airline-delay-cause-csv)
- **Mô tả:** Chứa thông tin chi tiết về các chuyến bay, hãng hàng không, sân bay và 5 nhóm nguyên nhân gây trễ (Air Carrier, Extreme Weather, National Aviation System, Late-arriving Aircraft, Security).

## 🛠 Công nghệ sử dụng
- **Backend:** [Polars](https://pola.rs/) (Xử lý dữ liệu cực nhanh với Lazy Queries).
- **Frontend:** [Dash Plotly](https://dash.plotly.com/) (Giao diện Dashboard tương tác).
- **Styling:** Dash Bootstrap Components (Dark Theme).
- **Visualization:** Plotly Express (Matrix Facet Charts).

## 🚀 Tính năng nổi bật trong Explorer
1. **Smart Dual-Filter:** Hệ thống lọc chéo (Circular Filter) giữa Hãng bay và Sân bay bằng `callback_context`.
2. **Matrix Analysis (Small Multiples):** Tự động dàn trang biểu đồ ma trận để so sánh hiệu suất giữa các hãng trên từng sân bay cụ thể.
3. **Dynamic Scaling:** Tự động tính toán chiều cao và khoảng cách (padding) biểu đồ dựa trên lượng dữ liệu được chọn để tránh đè chữ.
4. **Optimized UI:** Chú thích (Legend) được xếp dọc ở cuối trang và nhãn (Annotation) được nhấc bổng để tối ưu không gian hiển thị.

## 📂 Cấu trúc mã nguồn

```
root
├── app/               # Source code ứng dụng Dash (Layouts, Callbacks, Pages)
├── data/              # Dữ liệu thô (Raw data)
├── notebook/          # Scripts làm sạch và biến đổi dữ liệu (ETL)
├── output/            # Dữ liệu đã xử lý lưu dưới dạng .parquet (Polars-ready)
├── .venv/             # Môi trường ảo Python
├── requirements.txt   # Danh sách thư viện cần thiết
└── README.md          # Tài liệu hướng dẫn dự án thông minh.
```

# 🚀 Hướng dẫn cài đặt & Chạy

1. Thiết lập môi trường:

```bash
# Kích hoạt venv
.\.venv\Scripts\activate
# Cài đặt thư viện
pip install -r requirements.txt
```

2. Tiền xử lý dữ liệu: Chạy các scripts trong thư mục preprocessing/ để chuyển đổi dữ liệu từ data/ sang .parquet trong output/.

3. Khởi chạy Dashboard:

```bash
python -m app.server
```

---

## 📖 Hướng dẫn sử dụng
1. **Chọn Hãng bay:** Danh sách sân bay sẽ tự động co lại chỉ hiện các điểm đến của hãng đó.
2. **Chọn Sân bay:** Ngược lại, danh sách hãng sẽ chỉ hiện những ông có khai thác tại sân bay này.
3. **Chọn Thông số:** Có thể soi "Số lượng chuyến bay" hoặc "Thời gian trễ".
4. **Khám phá:** Bấm nút để hệ thống quét dữ liệu từ file Parquet và render ma trận biểu đồ.

---
