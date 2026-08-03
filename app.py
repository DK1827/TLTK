import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Tính lãi ngân hàng", page_icon="🏦")

st.title("🏦 TÍNH LÃI NGÂN HÀNG")

# ==========================
# Nhập dữ liệu
# ==========================

tien_gui = st.number_input(
    "💰 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500000000.0,
    step=1000000.0,
    format="%.0f"
)

lai_suat = st.number_input(
    "📈 Lãi suất (%)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

don_vi_lai = st.selectbox(
    "📌 Đơn vị lãi suất",
    [
        "Theo năm",
        "Theo tháng",
        "Theo ngày"
    ]
)

ngay_gui = st.date_input(
    "📅 Ngày gửi",
    value=date.today()
)

ngay_dao_han = st.date_input(
    "📅 Ngày đáo hạn",
    value=date.today()
)

# ==========================
# Tính toán
# ==========================

if ngay_dao_han > ngay_gui:

    # Khoảng cách thực tế
    rd = relativedelta(ngay_dao_han, ngay_gui)

    nam = rd.years
    thang = rd.months
    ngay = rd.days

    tong_ngay = (ngay_dao_han - ngay_gui).days

    # Quy đổi lãi suất về lãi suất theo ngày
    if don_vi_lai == "Theo năm":
        r = (lai_suat / 100) / 365

    elif don_vi_lai == "Theo tháng":
        r = (lai_suat / 100) / 30

    else:  # Theo ngày
        r = lai_suat / 100

    # Lãi đơn
    tong_lai_don = tien_gui * (1 + r * tong_ngay)
    lai_don = tong_lai_don - tien_gui

    # Lãi kép
    tong_lai_kep = tien_gui * ((1 + r) ** tong_ngay)
    lai_kep = tong_lai_kep - tien_gui

    # ==========================
    # Hiển thị kết quả
    # ==========================

    st.success(
        f"📅 Thời gian gửi: {nam} năm {thang} tháng {ngay} ngày"
    )

    st.info(
        f"⏳ Tổng số ngày gửi: {tong_ngay} ngày"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💵 Lãi đơn")

        st.metric(
            "Tiền lãi",
            f"{lai_don:,.0f} VNĐ"
        )

        st.metric(
            "Tổng tiền nhận",
            f"{tong_lai_don:,.0f} VNĐ"
        )

    with col2:
        st.subheader("💰 Lãi kép")

        st.metric(
            "Tiền lãi",
            f"{lai_kep:,.0f} VNĐ"
        )

        st.metric(
            "Tổng tiền nhận",
            f"{tong_lai_kep:,.0f} VNĐ"
        )

else:
    st.error("⚠️ Ngày đáo hạn phải lớn hơn ngày gửi.")
