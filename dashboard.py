import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="TRAVELOKA - Customer Clustering Dashboard")

# =========================================================
# 1. LOAD FILE
# =========================================================
FILES = {
    "lv1_clean":  "hotel_booking_cleaned_raw_with_clusters1.csv",
    "lv1_raw": "hotel_booking_cleaned_with_clusters1.csv",
    "lv2_clean":  "hotel_booking_cleaned_raw_with_clusters2.csv",
    "lv2_raw": "hotel_booking_cleaned_with_clusters2.csv",
    "clean":     "hotel_booking_cleaned.csv",
}

# =========================================================
# 1. LOAD FILE (CHỈ LV1)
# =========================================================
FILES_LV1 = {
    "lv1_clean": "hotel_booking_cleaned_raw_with_clusters1.csv",
    "lv1_raw":  "hotel_booking_cleaned_with_clusters1.csv",
}

def load_lv1():
    for key, f in FILES_LV1.items():
        try:
            df = pd.read_csv(f)
            return df, key, f
        except:
            pass
    return None, None, None

df, file_type, used_file = load_lv1()

if df is None:
    st.error("❌ Không tìm thấy file LV1. Hãy đặt file lv1_raw hoặc lv1_clean cùng thư mục dashboard.")
    st.stop()

st.sidebar.success(f"Đã load file LV1: **{used_file}**")
st.sidebar.info(f"Loại file nhận diện: **{file_type.upper()}**")

# =========================================================
# 2. CHUẨN HÓA TÊN CỘT (CHÍNH XÁC TUYỆT ĐỐI)
# =========================================================
rename_map = {}

# Chuẩn hoá ADR
if "room_price_per_night" in df.columns:
    rename_map["room_price_per_night"] = "adr"

# Lần 1: LOW–MID–HIGH
if file_type in ["lv1_raw", "lv1_clean"]:
    if "cluster" in df.columns:
        rename_map["cluster"] = "cluster_lvl1"
    if "Tên Cụm" in df.columns:
        rename_map["Tên Cụm"] = "cluster_lvl1"

# Lần 2: SUBCLUSTER của nhóm chi tiêu cao
if file_type in ["lv2_raw", "lv2_clean"]:
    if "subcluster" in df.columns:
        rename_map["subcluster"] = "cluster_lvl2"
    if "Cụm_Chi_Tiết" in df.columns:
        rename_map["Cụm_Chi_Tiết"] = "cluster_lvl2"

df = df.rename(columns=rename_map)

# =========================================================
# 3. TẠO CỘT HỖ TRỢ
# =========================================================
if "stays_in_week_nights" in df.columns and "stays_in_weekend_nights" in df.columns:
    df["total_nights"] = df["stays_in_week_nights"] + df["stays_in_weekend_nights"]

if "is_canceled" in df.columns:
    df["is_canceled_binary"] = (df["is_canceled"] > 0).astype(int)

# =========================================================
# 4. TỔNG QUAN
# =========================================================
st.title("📊 TRAVELOKA – Customer Clustering Dashboard")

col1, col2, col3 = st.columns(3)
total_booking = len(df)
avg_adr = df["adr"].mean() if "adr" in df.columns else 0
cancel_rate = df["is_canceled_binary"].mean() if "is_canceled_binary" in df.columns else 0

col1.metric("Tổng booking", f"{total_booking:,}")
col2.metric("ADR trung bình", f"{avg_adr:,.0f}")
col3.metric("Tỷ lệ huỷ phòng", f"{cancel_rate*100:.2f} %")

st.markdown("---")

# =========================================================
# 5. PHÂN CỤM LẦN 1 – INSIGHT VỀ CHI TIÊU
# =========================================================
if "cluster_lvl1" in df.columns: 
    st.header("1️⃣ Phân cụm lần 1 – Nhóm khách LOW / MID / HIGH")

    palette = {
        "Khách chi tiêu thấp": "#66c2a5",
        "Khách chi tiêu trung bình": "#fc8d62",
        "Khách chi tiêu cao": "#8da0cb",
    }

    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(df, x="cluster_lvl1", y="adr", palette=palette, ax=ax)

    # --- HIỆN GIÁ TRỊ TRÊN ĐẦU CỘT ---
    for p in ax.patches:
        value = p.get_height()
        ax.text(
            p.get_x() + p.get_width()/2,
            value,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    ax.set_title("ADR trung bình theo nhóm chi tiêu")
    ax.set_xlabel("")
    ax.set_ylabel("ADR")

    st.pyplot(fig)

    st.markdown("""
    ### 🔍 Nhận xét từ notebook:
    - **Chi tiêu thấp** → ADR thấp, nhu cầu cơ bản  
    - **Chi tiêu trung bình** → hành vi đa dạng  
    - **Chi tiêu cao** → ADR cao nhất, tổng đêm dài → khách có giá trị cao nhất  
    """)

  # -------------------------------
    # Kiểm tra bias phân cụm LV1
    # -------------------------------
    st.subheader("⚖️ Kiểm tra bias phân cụm LV1 – customer_type & market_segment")
    
    def cluster_bias_auto_st(df, cluster_col='cluster_lvl1'):
        customer_type_cols = [c for c in df.columns if c.startswith('customer_type_')]
        market_segment_cols = [c for c in df.columns if c.startswith('market_segment_')]

        if customer_type_cols or market_segment_cols:
            sensitive_cols = customer_type_cols + market_segment_cols
            bias_df = df.groupby(cluster_col)[sensitive_cols].mean().multiply(100).round(2)
            st.markdown(f"**Bảng phân bố % khách theo cluster (one-hot)**")
            st.dataframe(bias_df)
        else:
            sensitive_cols = [c for c in ['customer_type','market_segment'] if c in df.columns]
            for col in sensitive_cols:
                st.markdown(f"**{col} – % khách theo cluster**")
                bias_df = df.groupby(cluster_col)[col].value_counts(normalize=True).unstack().multiply(100).round(2)
                st.dataframe(bias_df)

    cluster_bias_auto_st(df, cluster_col='cluster_lvl1')

    st.markdown("""
#### Nhận xét bias LV1:
- **Customer_type:** Transient chiếm đa số; Transient-Party cao ở cluster chi tiêu thấp; Contract/Group chiếm ít nhưng cluster chi tiêu cao có Contract cao hơn.
- **Market_segment:** Online TA phổ biến; Offline TA/TO cao ở cluster chi tiêu cao; Corporate cao hơn ở cluster chi tiêu thấp; Direct chiếm cao ở cluster chi tiêu thấp.
- **Kết luận:** Cluster chi tiêu cao → Transient + Online/Offline TA/TO; Cluster chi tiêu thấp → Transient-Party + Corporate/Direct.
""")

    # -------------------------------
    # Chọn cụm LV1 để xem chi tiết numeric
    # -------------------------------
    chosen = st.selectbox("📍 Chọn cụm LV1 để xem sâu:", df["cluster_lvl1"].unique())
    sub = df[df["cluster_lvl1"] == chosen]

    c1, c2, c3 = st.columns(3)
    if "adr" in df:        c1.plotly_chart(px.histogram(sub, x="adr", title="ADR"))
    if "lead_time" in df:  c2.plotly_chart(px.histogram(sub, x="lead_time", title="Lead Time"))
    if "total_nights" in df: c3.plotly_chart(px.histogram(sub, x="total_nights", title="Total Nights"))

    st.markdown("---")




# =========================================================
# 6. PHÂN CỤM LẦN 2 – NHÓM HÀNH VI KHÁCH CHI TIÊU CAO
# =========================================================
# =========================================================
# 1. LOAD FILE (CHỈ LV2)
# =========================================================
FILES_LV2 = {
    "lv2_clean": "hotel_booking_cleaned_raw_with_clusters2.csv",
    "lv2_raw":  "hotel_booking_cleaned_with_clusters2.csv",
}

def load_lv2():
    for key, f in FILES_LV2.items():
        try:
            df = pd.read_csv(f)
            return df, key, f
        except:
            pass
    return None, None, None

df_lv2, file_type_lv2, used_file_lv2 = load_lv2()

if df_lv2 is None:
    st.error("❌ Không tìm thấy file LV2. Hãy đặt file lv2_raw hoặc lv2_clean cùng thư mục dashboard.")
    st.stop()

st.sidebar.success(f"Đã load file LV2: **{used_file_lv2}**")
st.sidebar.info(f"Loại file nhận diện: **{file_type_lv2.upper()}**")

# =========================
# Rename cột nếu cần
# =========================
rename_map = {}
if file_type_lv2 in ["lv2_raw", "lv2_clean"]:
    if "subcluster" in df_lv2.columns:
        rename_map["subcluster"] = "cluster_lvl2"
    if "Tên_Cụm_Chi_Tiết" in df_lv2.columns:
        rename_map["Tên_Cụm_Chi_Tiết"] = "cluster_lvl2"

df_lv2 = df_lv2.rename(columns=rename_map)

# Kiểm tra xem cột cluster_lvl2 có tồn tại chưa
if "cluster_lvl2" not in df_lv2.columns:
    st.warning("⚠️ Dữ liệu LV2 không có cột 'cluster_lvl2'. Phần phân tích LV2 sẽ bị bỏ qua.")
else:
    # =========================
    # Tiếp tục xử lý LV2
    # =========================
    st.header("2️⃣ Phân cụm lần 2 – Nhóm hành vi của khách chi tiêu cao")

    df = df_lv2.copy()

    # Làm sạch chuỗi chống lỗi filter
    df["cluster_lvl2"] = (
        df["cluster_lvl2"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


    # Tính tổng khách và tỉ lệ hủy phòng
    total_hv = len(df)
    cancel_rate = df['is_canceled'].mean() * 100

    # Hiển thị cùng hàng
    col1, col2 = st.columns(2)
    col1.metric("Tổng khách chi tiêu cao (LV2)", f"{total_hv:,}")
    col2.metric("Tỉ lệ hủy phòng", f"{cancel_rate:.2f}%")

    st.write("""
    ### 🧭 Ý nghĩa phân cụm đợt 2
    Đây là phân đoạn hành vi **chỉ trong nhóm khách chi tiêu cao**, ví dụ:
    - HV – Công tác  
    - HV – Gia đình  
    - HV – Du lịch dài ngày  
    - HV – Đặt gấp  
    """)
    # Tạo cột để hiển thị 3 biểu đồ cùng hàng
    cols = st.columns(3)

    # Tính total_nights nếu chưa có
    if 'total_nights' not in df.columns:
        df['total_nights'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']

    # Biểu đồ 1: ADR
    fig_adr = px.histogram(df, x='adr', nbins=30, title="Phân bố giá phòng trung bình (ADR)", 
                        labels={'adr':'ADR'}, marginal="box")
    cols[0].plotly_chart(fig_adr, use_container_width=True)

    # Biểu đồ 2: Tổng số đêm lưu trú
    fig_nights = px.histogram(df, x='total_nights', nbins=30, title="Phân bố số đêm lưu trú", 
                            labels={'total_nights':'Số đêm'}, marginal="box")
    cols[1].plotly_chart(fig_nights, use_container_width=True)

    # Biểu đồ 3: Lead time (số ngày đặt trước)
    fig_lead = px.histogram(df, x='lead_time', nbins=30, title="Số ngày đặt trước", 
                            labels={'lead_time':'Đặt trước (ngày)'}, marginal="box")
    cols[2].plotly_chart(fig_lead, use_container_width=True)

 # ============================
# HIỂN THỊ HÀNH VI TẤT CẢ CỤM LV2
# ============================

clusters2 = sorted(df["cluster_lvl2"].unique())

st.header("📌 Hành vi của tất cả các cụm hành vi (LV2)")

numeric_cols = ["adr", "lead_time", "total_nights"]
numeric_cols = [c for c in numeric_cols if c in df.columns]

cat_cols = [
    "market_segment",
    "distribution_channel",
    "customer_type",
    "deposit_type",
    "reserved_room_type",
]
cat_cols = [c for c in cat_cols if c in df.columns]

# Lặp từng cụm
for cl in clusters2:
    st.subheader(f"🔹 **Cụm hành vi: {cl}**")

    df_sel = df[df["cluster_lvl2"] == cl].copy()

    # ============================
    # Numeric plots
    # ============================
    if numeric_cols:
        st.markdown("**📊 Phân bố các biến numeric:**")
        
        # Ensure numeric
        for col in numeric_cols:
            df_sel[col] = pd.to_numeric(df_sel[col], errors="coerce")
        df_sel_num = df_sel.dropna(subset=numeric_cols)

        cols_per_row = 3
        rows = (len(numeric_cols) + cols_per_row - 1) // cols_per_row

        for r in range(rows):
            row_cols = st.columns(cols_per_row)
            for i, col_name in enumerate(numeric_cols[r*cols_per_row:(r+1)*cols_per_row]):
                fig = px.histogram(
                    df_sel_num,
                    x=col_name,
                    nbins=30,
                    title=f"{col_name} – {cl}"
                )
                row_cols[i].plotly_chart(fig)

    # ============================
    # Categorical plots
    # ============================
    if cat_cols:
        st.markdown("**📊 Phân bố các thuộc tính categorical:**")

        for c in cat_cols:
            freq = (
                df_sel[c]
                .astype(str)
                .value_counts(normalize=True)
                .reset_index()
            )
            freq.columns = [c, "percent"]
            freq["percent"] = (freq["percent"] * 100).round(2)

            fig = px.bar(
                freq,
                x=c, y="percent", text="percent",
                title=f"Phân bố {c} – {cl}"
            )
            st.plotly_chart(fig)

    st.markdown("---")
# =========================================================
# 7. RADAR CHART & NHẬN XÉT – NHÓM KHÁCH CHI TIÊU CAO
# =========================================================
import plotly.graph_objects as go

# Chỉ hiển thị khi có dữ liệu LV2
if "cluster_lvl2" in df.columns:
    st.subheader("📈 Radar Chart – So sánh hành vi chi tiết của nhóm chi tiêu cao")

    # --- 1) Chọn các biến numeric quan trọng ---
    sub_numeric = ["adr", "room_price_total", "total_nights", "lead_time", "total_of_special_requests"]
    sub_numeric = [c for c in sub_numeric if c in df.columns]

    if not sub_numeric:
        st.warning("⚠️ Không có biến numeric phù hợp để vẽ radar chart.")
    else:
        # --- 2) Tạo summary trung bình theo cụm chi tiết ---
        summary2 = df.groupby('cluster_lvl2')[sub_numeric].mean()

        # --- 3) Gán tên chi tiết theo logic ---
        thr_adr    = summary2['adr'].quantile(0.8)
        thr_price  = summary2['room_price_total'].quantile(0.8) if 'room_price_total' in summary2 else summary2['adr'].quantile(0.8)
        thr_nights = summary2['total_nights'].quantile(0.8)
        thr_lead   = summary2['lead_time'].quantile(0.8)
        thr_req    = summary2['total_of_special_requests'].quantile(0.8)

        detail_labels = {}
        for cid in summary2.index:
            adr_val   = summary2.loc[cid, 'adr']
            price_val = summary2.loc[cid, 'room_price_total'] if 'room_price_total' in summary2 else adr_val
            nights_val= summary2.loc[cid, 'total_nights']
            lead_val  = summary2.loc[cid, 'lead_time']
            req_val   = summary2.loc[cid, 'total_of_special_requests']

            if (adr_val > thr_adr) and (price_val > thr_price) and (nights_val > thr_nights):
                detail_labels[cid] = "Luxury / Premium"
            elif (req_val > thr_req) or (lead_val > thr_lead):
                detail_labels[cid] = "Nhu cầu cao / Kỳ vọng cao"
            else:
                detail_labels[cid] = "Đi công tác / Gia đình / Tiêu chuẩn"

        df['Tên_Cụm_Chi_Tiết'] = df['cluster_lvl2'].map(detail_labels)

        # --- 4) Tạo summary chuẩn hóa để vẽ radar ---
        summary_detail = df.groupby('Tên_Cụm_Chi_Tiết')[sub_numeric].mean()
        summary_norm = (summary_detail - summary_detail.min()) / (summary_detail.max() - summary_detail.min())

        categories = summary_norm.columns.tolist()

        # --- 5) Vẽ radar chart ---
        fig = go.Figure()
        for cluster in summary_norm.index:
            values = summary_norm.loc[cluster].tolist()
            values += values[:1]  # vòng lại
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=cluster,
                marker=dict(symbol='circle')
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,1])
            ),
            showlegend=True,
            title="Radar Chart – Hành vi chi tiết nhóm chi tiêu cao"
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- 6) Nhận xét chi tiết ---
        st.markdown("""
### 📝 Nhận xét theo nhóm chi tiêu cao

**1. Luxury / Premium → Khách đẳng cấp nhất**
- ADR rất cao → chọn phòng cao cấp, suite, premium.
- Tổng tiền phòng cao → lưu trú dài hoặc đặt phòng đắt.
- Số đêm lưu trú dài → traveling for leisure, nghỉ dưỡng.
- Lead time cực cao → khách lên kế hoạch, đặt trước xa.
- Yêu cầu đặc biệt vừa phải → nhu cầu đặc biệt không nhiều.

**2. Nhu cầu cao / Kỳ vọng cao → Đặt trước không xa nhưng nhiều yêu cầu đặc biệt**
- Rất nhiều yêu cầu đặc biệt → khách kén chọn, yêu cầu dịch vụ cao.
- Lead time trung bình → không đặt quá sớm.
- ADR trung bình → không phải nhóm luxury nhưng kỳ vọng cao.
- Room price tổng trung bình → ngân sách vừa phải.
- Số đêm lưu trú thấp → chuyến đi ngắn, có thể business trip hoặc weekend trip.

**3. Đi công tác / Gia đình / Tiêu chuẩn → Khách đơn giản – lưu trú ngắn – chi tiêu thấp**
- Điểm trên mọi biến đều thấp → không phải high spender.
- Lead time ngắn → đặt gần ngày đi, last-minute booking.
- Số đêm trung bình thấp → chủ yếu 1–2 đêm.
- Yêu cầu đặc biệt thấp → ít nhu cầu cá nhân hóa.
""")


# =========================================================
# 8. HEATMAP & NHẬN XÉT – NHÓM KHÁCH CHI TIÊU CAO
# =========================================================
import matplotlib.pyplot as plt
import seaborn as sns

st.subheader("🌡️ Heatmap – Hành vi chi tiết nhóm chi tiêu cao")

# Vẽ heatmap
plt.figure(figsize=(12,6))
sns.heatmap(summary_norm, annot=True, cmap='YlGnBu', fmt=".2f")
plt.title("Heatmap hành vi của nhóm chi tiêu cao")
st.pyplot(plt.gcf())  # streamlit hiển thị figure hiện tại
plt.close()

# Nhận xét chi tiết
st.markdown("""
### 📝 Nhận xét theo heatmap

**1. Phân khúc Luxury / Premium (Sang trọng / Cao cấp)**
- Giá phòng (`adr`, `room_price_total`): Giá trị ~1 → chi tiêu cao và đồng nhất nhất.
- Thời gian lưu trú (`total_nights`): Giá trị ~1 → lưu trú dài hoặc ổn định.
- Lead time (`lead_time`): Giá trị ~1 → đặt trước lâu, ổn định.
- Yêu cầu đặc biệt (`total_of_special_requests`): Giá trị ~0.3 → ít yêu cầu đặc biệt, dịch vụ tiêu chuẩn đã thỏa mãn.

**2. Phân khúc Nhu cầu cao / Kỳ vọng cao (High Demand / High Expectation)**
- Yêu cầu đặc biệt (`total_of_special_requests`): Giá trị ~1 → thường xuyên yêu cầu đặc biệt.
- Giá phòng (`adr`): Giá trị ~0.47 → chi tiêu trung bình, không cao bằng Luxury/Premium.
- Thời gian lưu trú (`total_nights`): Giá trị ~0 → lưu trú ngắn.
- Lead time (`lead_time`): Giá trị ~0.13 → đặt phòng gấp hơn nhóm khác.

**3. Phân khúc Đi công tác / Gia đình / Tiêu chuẩn (Business / Family / Standard)**
- Thời gian lưu trú (`total_nights`): Giá trị ~0.56 → yếu tố chính kéo tổng chi tiêu cao.
- Các thông số khác: Giá trị ~0 → đặt trước ngắn, chi tiêu ADR thấp, ít yêu cầu đặc biệt.
""")



st.subheader("⚖️ Kiểm tra bias phân cụm theo customer_type & market_segment")

def cluster_bias_auto_st(df, cluster_col='Tên_Cụm'):
    """
    Kiểm tra bias trong phân cụm cho các biến nhạy cảm
    - Hiển thị bảng % khách theo cluster
    """
    # --- Nhận diện cột one-hot ---
    customer_type_cols = [c for c in df.columns if c.startswith('customer_type_')]
    market_segment_cols = [c for c in df.columns if c.startswith('market_segment_')]

    if customer_type_cols or market_segment_cols:
        # Dữ liệu đã one-hot
        sensitive_cols = customer_type_cols + market_segment_cols
        bias_df = df.groupby(cluster_col)[sensitive_cols].mean().multiply(100).round(2)
        st.markdown(f"**Bảng phân bố % khách theo cluster (one-hot)**")
        st.dataframe(bias_df)
    else:
        # Dữ liệu gốc
        sensitive_cols = [c for c in ['customer_type','market_segment'] if c in df.columns]
        for col in sensitive_cols:
            st.markdown(f"**{col} – % khách theo cluster**")
            bias_df = df.groupby(cluster_col)[col].value_counts(normalize=True).unstack().multiply(100).round(2)
            st.dataframe(bias_df)

# ===== Block 2: Lần 2 (chi tiết khách chi tiêu cao) =====
if "Tên_Cụm_Chi_Tiết" in df.columns:
    st.markdown("### 📌 LẦN 2: Phân cụm chi tiết khách chi tiêu cao")
    cluster_bias_auto_st(df, cluster_col='Tên_Cụm_Chi_Tiết')
    st.markdown("""
#### Nhận xét Lần 2:
- **Customer_type:** Transient vẫn chiếm đa số; Đi công tác/Gia đình/Tiêu chuẩn có Contract cao hơn; Transient-Party cao nhất ở nhóm này; Luxury/Premium & Nhu cầu cao tập trung Transient, ít Contract/Group.
- **Market_segment:** Luxury/Premium & Nhu cầu cao → chủ yếu Online TA; Đi công tác/Gia đình/Tiêu chuẩn → Offline TA/TO và Online TA gần bằng nhau; các kênh khác rất ít.
- **Kết luận:** Cluster chi tiết tách rõ hành vi và kênh đặt:
    - Luxury / Premium → khách chi tiêu cao, chủ yếu Transient, đặt trực tuyến.
    - Nhu cầu cao / Kỳ vọng cao → khách chi tiêu cao, Online TA chủ yếu.
    - Đi công tác / Gia đình / Tiêu chuẩn → khách đa dạng, nhiều Contract/Offline TA/TO.
- Bias vẫn hợp lý, cluster phản ánh đúng đặc điểm loại khách và kênh đặt.
""")
