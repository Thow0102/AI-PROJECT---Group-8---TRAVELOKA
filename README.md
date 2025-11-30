# AI-PROJECT---Group-8---TRAVELOKA
***Đề tài***: ỨNG DỤNG MACHINE LEARNING TRONG PHÂN KHÚC KHÁCH HÀNG VÀ DỰ BÁO NHÓM CHI TIÊU CAO TRÊN NỀN TẢNG TRAVELOKA

## Giới thiệu
Dự án nhằm xây dựng mô hình phân cụm (K-Means) để xác định nhóm khách hàng có hành vi chi tiêu cao dựa trên dữ liệu đặt phòng của Traveloka, giúp tối ưu chiến dịch marketing và tăng doanh thu trung bình mỗi khách hàng.

## Thành viên nhóm
| Họ tên | MSSV | Vai trò |
|--------|-------|----------|
| Mai Sĩ Thơ | 31231024231 | Nhóm trưởng – Data Modeling, GitHub |
| Hà Ngọc Phương | 31231024954 | Data Cleaning & Preprocessing |
| Trần Thị Thanh Vi | 31231026955 | EDA & Visualization |
| Ngô Thị Khánh Ngọc | 31231021734 | Business Analyst – AI Canvas, KPI |
| Nguyễn Thị Kim Ngân | 31231022496 | Documentation & Report |
| Trương Bảo Hân | 31231020211 | Design & Presentation |
| Võ Nguyễn Hoàng Nhi | 31231026034 | Communication & Marketing Strategy |

## Cấu trúc các file trong đồ án
├── data/
│   ├── hotel_booking_demand.csv                         # Dữ liệu gốc từ Kaggle
│   ├── hotel_booking_cleaned_raw_with_clusters1.csv     # Dữ liệu phân cụm lần 1 (chưa chuẩn hóa)
│   ├── hotel_booking_cleaned_raw_with_clusters2.csv     # Dữ liệu phân cụm lần 2 (chưa chuẩn hóa)
│   ├── hotel_booking_cleaned_with_clusters1.csv         # Dữ liệu sạch phân cụm lần 1 (đã chuẩn hóa)
│   └── hotel_booking_cleaned_with_clusters2.csv         # Dữ liệu sạch phân cụm lần 2 (đã chuẩn hóa)
│
├── notebooks/
│   └── codeAIPj.ipynb                                   # Notebook xử lý & phân tích dữ liệu
│
├── src/
│   └── dashboard.py                                     # Mã nguồn Dashboard
│
├── reports/
│   ├── Nhom8_report.pdf                                 # Báo cáo cuối cùng của dự án
│   ├── SLIDE FINAL AI PROJECT.pdf                       # Slide thuyết trình
│   └── brochure.pdf                                     # Brochure giới thiệu kết quả
│
└── README.md                                            # Tài liệu mô tả dự án


## Mục tiêu dự án
- Phân tích hành vi khách hàng từ dữ liệu `Hotel Booking Demand`.
- Áp dụng thuật toán **K-Means Clustering, BIRCH Clustering, DBSCAN Clustering** để tìm nhóm khách hàng có chi tiêu cao.
- Đưa ra chiến lược marketing phù hợp với từng phân khúc.
- Đánh giá hiệu quả mô hình theo các chỉ số như **Silhouette Score** và **ROI tiềm năng**.

## Mô hình & Công cụ
- **Ngôn ngữ:** Python (Pandas, NumPy, Scikit-learn)
- **Công cụ:** Jupyter Notebook
- **Framework:** CPMAI + Agile/Scrum

## Tiến độ
| Sprint | Thời gian | Deliverables |
|--------|------------|--------------|
| 1 | 06/10/2025 - 22/10/2025 | Business Understanding, AI Canvas, KPI |
| 2 | 23/10/2025 - 06/11/2025 | EDA, Feature Set, Baseline Model |
| 3 | 07/11/2025 - 16/11/2025 | Model tuning, ROI Evaluation |
| 4 | 17/11/2025 - 30/11/2025 | Dashboard, Final Report, Slide |

## Liên kết
- Trang Notion nhóm: https://www.notion.so/294862272ad48053934fd79c3ff07679?v=294862272ad481029321000c5691a819&source=copy_link
- Dataset gốc_Hotel Booking Demand on Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

## Kết quả dự kiến
- Độ chính xác dự đoán phân khúc cao cấp ≥ 85%
- Tăng doanh thu bình quân mỗi khách hàng cao cấp 10–15%
- Tỷ lệ giữ chân khách hàng cao cấp tăng 10–12%

## Kết quả chính của dự án
- Xác định **3 phân khúc khách hàng giá trị cao**:
  - **Luxury / Premium**
  - **Nhu cầu cao / Kỳ vọng cao**
  - **Gia đình – Công tác – Tiêu chuẩn**
- Tính khả thi tài chính:
  - **ROI:** 151.4%  
  - **NPV:** +43.1 tỷ VND  
  - **IRR:** 63.8%  
- Dashboard trình bày trực quan các phân khúc khách hàng
- Gợi ý chiến lược marketing cho từng nhóm

