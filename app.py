import streamlit as st
from datetime import date

st.set_page_config(page_title="Tính lãi ngân hàng", page_icon="🏦")

st.title("🏦 TÍNH LÃI NGÂN HÀNG")

# Nhập dữ liệu
tien_gui = st.number_input(
    "💰 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500000000.0,
    step=1000000.0,
    format="%.0f"
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

ngay_gui = st.date_input(
    "📅 Ngày gửi",
    value=date.today()
)

ngay_rut = st.date_input(
    "📅 Ngày rút",
    value=date.today()
)

if ngay_rut >= ngay_gui:

    so_ngay = (ngay_rut - ngay_gui).days

    r = (lai_suat / 100) / 365

    # Lãi đơn
    tong_lai_don = tien_gui * (1 + r * so_ngay)
    lai_don = tong_lai_don - tien_gui

    # Lãi kép
    tong_lai_kep = tien_gui * ((1 + r) ** so_ngay)
    lai_kep = tong_lai_kep - tien_gui

    st.divider()

    st.subheader("📊 KẾT QUẢ")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Lãi đơn")

        st.metric(
            "Tiền lãi",
            f"{lai_don:,.0f} VNĐ"
        )

        st.metric(
            "Tổng nhận",
            f"{tong_lai_don:,.0f} VNĐ"
        )

    with col2:
        st.success("Lãi kép")

        st.metric(
            "Tiền lãi",
            f"{lai_kep:,.0f} VNĐ"
        )

        st.metric(
            "Tổng nhận",
            f"{tong_lai_kep:,.0f} VNĐ"
        )

    st.info(f"📅 Số ngày gửi: **{so_ngay} ngày**")

else:
    st.error("Ngày rút phải lớn hơn hoặc bằng ngày gửi.")
