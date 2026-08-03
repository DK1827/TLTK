import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

st.title("🏦 TÍNH LÃI NGÂN HÀNG")

# Nhập dữ liệu
tien_gui = st.number_input(
    "💰 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500000000.0,
    step=1000000.0
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

ngay_gui = st.date_input("📅 Ngày gửi", date.today())
ngay_dao_han = st.date_input("📅 Ngày đáo hạn", date.today())

if ngay_dao_han > ngay_gui:

    # Khoảng cách thực tế
    rd = relativedelta(ngay_dao_han, ngay_gui)

    nam = rd.years
    thang = rd.months
    ngay = rd.days

    # Tổng số ngày thực tế
    tong_ngay = (ngay_dao_han - ngay_gui).days

    r = (lai_suat / 100) / 365

    # Lãi đơn
    tong_lai_don = tien_gui * (1 + r * tong_ngay)
    lai_don = tong_lai_don - tien_gui

    # Lãi kép
    tong_lai_kep = tien_gui * ((1 + r) ** tong_ngay)
    lai_kep = tong_lai_kep - tien_gui

    st.success(f"Thời gian gửi: {nam} năm {thang} tháng {ngay} ngày")
    st.info(f"Tổng số ngày: {tong_ngay} ngày")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Lãi đơn")
        st.write(f"Tiền lãi: **{lai_don:,.0f} VNĐ**")
        st.write(f"Tổng nhận: **{tong_lai_don:,.0f} VNĐ**")

    with col2:
        st.subheader("Lãi kép")
        st.write(f"Tiền lãi: **{lai_kep:,.0f} VNĐ**")
        st.write(f"Tổng nhận: **{tong_lai_kep:,.0f} VNĐ**")

else:
    st.error("Ngày đáo hạn phải lớn hơn ngày gửi.")
