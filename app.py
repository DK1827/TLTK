import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Tính lãi ngân hàng", page_icon="🏦")

st.title("🏦 TÍNH LÃI NGÂN HÀNG")

# ==========================
# NHẬP DỮ LIỆU
# ==========================

tien_gui = st.number_input(
    "💰 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500000000.0,
    step=1000000.0,
    format="%.0f"
)

# Lãi suất có kỳ hạn
lai_suat_co_ky_han = st.number_input(
    "📈 Lãi suất có kỳ hạn (%)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

# Lãi suất không kỳ hạn
lai_suat_khong_ky_han = st.number_input(
    "📈 Lãi suất không kỳ hạn (%)",
    min_value=0.0,
    value=0.2,
    step=0.01
)

# Đơn vị lãi suất
don_vi_lai = st.selectbox(
    "📌 Đơn vị lãi suất",
    [
        "Theo năm",
        "Theo tháng",
        "Theo ngày"
    ]
)

# Ngày gửi
ngay_gui = st.date_input(
    "📅 Ngày gửi",
    value=date.today()
)

# Ngày đến hạn
ngay_den_han = st.date_input(
    "📅 Ngày đến hạn",
    value=date.today()
)

# Ngày rút tiền
ngay_rut_tien = st.date_input(
    "💵 Ngày rút tiền",
    value=ngay_den_han
)

# ==========================
# TÍNH TOÁN
# ==========================

if ngay_rut_tien >= ngay_gui:

    rd = relativedelta(ngay_rut_tien, ngay_gui)

    nam = rd.years
    thang = rd.months
    ngay = rd.days

    tong_ngay = (ngay_rut_tien - ngay_gui).days

    # ==========================
    # XÁC ĐỊNH LÃI SUẤT ÁP DỤNG
    # ==========================

    if ngay_rut_tien < ngay_den_han:

        st.warning("⚠️ Rút trước hạn - áp dụng lãi suất không kỳ hạn.")

        lai_suat_ap_dung = lai_suat_khong_ky_han
        ten_lai = "Không kỳ hạn"

    else:

        lai_suat_ap_dung = lai_suat_co_ky_han
        ten_lai = "Có kỳ hạn"

    # ==========================
    # QUY ĐỔI LÃI SUẤT
    # ==========================

    if don_vi_lai == "Theo năm":
        r = (lai_suat_ap_dung / 100) / 365

    elif don_vi_lai == "Theo tháng":
        r = (lai_suat_ap_dung / 100) / 30

    else:
        r = lai_suat_ap_dung / 100

    # ==========================
    # TÍNH LÃI ĐƠN
    # ==========================

    tong_lai_don = tien_gui * (1 + r * tong_ngay)
    lai_don = tong_lai_don - tien_gui

    # ==========================
    # TÍNH LÃI KÉP
    # ==========================

    tong_lai_kep = tien_gui * ((1 + r) ** tong_ngay)
    lai_kep = tong_lai_kep - tien_gui

    # ==========================
    # HIỂN THỊ KẾT QUẢ
    # ==========================

    st.success(
        f"📅 Thời gian gửi: {nam} năm {thang} tháng {ngay} ngày"
    )

    st.info(f"📅 Ngày gửi: {ngay_gui.strftime('%d/%m/%Y')}")
    st.info(f"📅 Ngày đến hạn: {ngay_den_han.strftime('%d/%m/%Y')}")
    st.info(f"💵 Ngày rút tiền: {ngay_rut_tien.strftime('%d/%m/%Y')}")

    st.info(f"⏳ Tổng số ngày gửi: {tong_ngay} ngày")

    st.write(f"📌 Loại lãi suất áp dụng: **{ten_lai}**")
    st.write(f"📈 Lãi suất áp dụng: **{lai_suat_ap_dung:.2f}% ({don_vi_lai})**")

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
    st.error("⚠️ Ngày rút tiền phải lớn hơn hoặc bằng ngày gửi.")
