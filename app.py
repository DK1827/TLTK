import streamlit as st

st.title("🏦 TÍNH LÃI NGÂN HÀNG")

# Nhập dữ liệu
tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500000000.0,
    step=1000000.0
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

st.subheader("Thời gian gửi")

col1, col2, col3 = st.columns(3)

with col1:
    nam = st.number_input("Năm", min_value=0, value=0)

with col2:
    thang = st.number_input("Tháng", min_value=0, max_value=11, value=3)

with col3:
    ngay = st.number_input("Ngày", min_value=0, max_value=31, value=2)

# Quy đổi
tong_ngay = nam * 365 + thang * 30 + ngay

r = (lai_suat / 100) / 365

tong_lai_don = tien_gui * (1 + r * tong_ngay)
lai_don = tong_lai_don - tien_gui

tong_lai_kep = tien_gui * ((1 + r) ** tong_ngay)
lai_kep = tong_lai_kep - tien_gui

st.divider()

st.write(f"**Tổng thời gian gửi:** {nam} năm {thang} tháng {ngay} ngày")
st.write(f"**Quy đổi:** {tong_ngay} ngày")

col1, col2 = st.columns(2)

with col1:
    st.success("Lãi đơn")
    st.metric("Tiền lãi", f"{lai_don:,.0f} VNĐ")
    st.metric("Tổng nhận", f"{tong_lai_don:,.0f} VNĐ")

with col2:
    st.success("Lãi kép")
    st.metric("Tiền lãi", f"{lai_kep:,.0f} VNĐ")
    st.metric("Tổng nhận", f"{tong_lai_kep:,.0f} VNĐ")
