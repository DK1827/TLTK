# =========================================================
# BÀI TẬP TRÊN LỚP
# =========================================================

st.divider()

st.header("📝 BÀI TẬP TRÊN LỚP")

st.markdown("""
**Dữ liệu bài toán:**

- Số tiền gửi: **500.000.000 VNĐ**
- Ngày gửi: **23/08/2026**
- Kỳ hạn: **3 tháng**
- Ngày đáo hạn: **23/11/2026**
- Lãi suất có kỳ hạn: **5%/năm**
- Lãi suất không kỳ hạn: **0,2%/năm**
- Phương thức nhận lãi: **Cuối kỳ**
""")

# ---------------------------------------------------------
# DỮ LIỆU CỐ ĐỊNH CỦA ĐỀ
# ---------------------------------------------------------

tien_de = 500_000_000

ngay_gui_de = date(2026, 8, 23)

ky_han_de = 3

ngay_dao_han_de = ngay_gui_de + relativedelta(
    months=ky_han_de
)

lai_suat_co_ky_han_de = 5.0

lai_suat_khong_ky_han_de = 0.2

lai_suat_vay_de = 8.0


# =========================================================
# HÀM TÍNH LÃI THEO NGÀY
# =========================================================

def tinh_lai_de(so_tien, lai_suat, ngay_bat_dau, ngay_ket_thuc):
    so_ngay = (ngay_ket_thuc - ngay_bat_dau).days

    lai = (
        so_tien
        * lai_suat / 100
        * so_ngay / 365
    )

    return so_ngay, lai


# =========================================================
# CÂU 1
# RÚT ĐÚNG HẠN 23/11/2026
# =========================================================

st.subheader("🔹 Câu 1. Rút đúng ngày đáo hạn")

so_ngay_1, lai_1 = tinh_lai_de(
    tien_de,
    lai_suat_co_ky_han_de,
    ngay_gui_de,
    ngay_dao_han_de
)

tong_tien_1 = tien_de + lai_1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Số ngày gửi",
        f"{so_ngay_1} ngày"
    )

with col2:
    st.metric(
        "Tiền lãi",
        dinh_dang_tien(lai_1)
    )

with col3:
    st.metric(
        "Tổng tiền nhận",
        dinh_dang_tien(tong_tien_1)
    )

st.info(
    f"""
    **Công thức:**

    Tiền lãi = 500.000.000 × 5% × {so_ngay_1}/365

    **Tiền lãi = {dinh_dang_tien(lai_1)}**

    **Tổng tiền nhận = {dinh_dang_tien(tong_tien_1)}**
    """
)


# =========================================================
# CÂU 2
# RÚT NGÀY 26/09/2026
# =========================================================

st.subheader("🔹 Câu 2. Rút ngày 26/09/2026")

ngay_rut_2 = date(2026, 9, 26)

so_ngay_2, lai_2 = tinh_lai_de(
    tien_de,
    lai_suat_khong_ky_han_de,
    ngay_gui_de,
    ngay_rut_2
)

tong_tien_2 = tien_de + lai_2

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Số ngày gửi",
        f"{so_ngay_2} ngày"
    )

with col2:
    st.metric(
        "Tiền lãi",
        dinh_dang_tien(lai_2)
    )

with col3:
    st.metric(
        "Tổng tiền nhận",
        dinh_dang_tien(tong_tien_2)
    )

st.warning(
    f"""
    ⚠️ Khách hàng rút trước hạn nên toàn bộ thời gian gửi
    được tính theo lãi suất không kỳ hạn **0,2%/năm**.

    Tiền lãi: **{dinh_dang_tien(lai_2)}**

    Tổng tiền nhận: **{dinh_dang_tien(tong_tien_2)}**
    """
)


# =========================================================
# CÂU 3
# RÚT NGÀY 10/10/2026
# =========================================================

st.subheader("🔹 Câu 3. Rút ngày 10/10/2026")

ngay_rut_3 = date(2026, 10, 10)

so_ngay_3, lai_3 = tinh_lai_de(
    tien_de,
    lai_suat_khong_ky_han_de,
    ngay_gui_de,
    ngay_rut_3
)

tong_tien_3 = tien_de + lai_3

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Số ngày gửi",
        f"{so_ngay_3} ngày"
    )

with col2:
    st.metric(
        "Tiền lãi",
        dinh_dang_tien(lai_3)
    )

with col3:
    st.metric(
        "Tổng tiền nhận",
        dinh_dang_tien(tong_tien_3)
    )

st.warning(
    f"""
    ⚠️ Khách hàng rút trước hạn nên áp dụng lãi suất
    không kỳ hạn **0,2%/năm**.

    Tiền lãi: **{dinh_dang_tien(lai_3)}**

    Tổng tiền nhận: **{dinh_dang_tien(tong_tien_3)}**
    """
)


# =========================================================
# CÂU 4
# KHÁCH HÀNG CẦN 500 TRIỆU NGÀY 26/11/2026
# =========================================================

st.subheader(
    "🔹 Câu 4. Tư vấn khách hàng ngày 26/11/2026"
)

ngay_can_tien = date(2026, 11, 26)

so_tien_can = 500_000_000

# Tiền gửi nếu giữ đến ngày đáo hạn
tien_nhan_dao_han = tong_tien_1

# Phần tiền còn lại sau khi lấy 500 triệu
tien_du = tien_nhan_dao_han - so_tien_can

st.write(
    f"""
    Ngày **26/11/2026**, khách hàng cần **500.000.000 VNĐ**.

    Nếu khách hàng giữ khoản tiền gửi đến ngày đáo hạn
    **23/11/2026**, số tiền nhận được là:

    **{dinh_dang_tien(tien_nhan_dao_han)}**
    """
)

if tien_nhan_dao_han >= so_tien_can:

    st.success(
        f"""
        ✅ **Phương án có lợi nhất:**

        Khách hàng nên **giữ tiền gửi đến ngày đáo hạn**,
        sau đó sử dụng tiền để đáp ứng nhu cầu 500 triệu.

        - Tiền nhận khi đáo hạn:
          **{dinh_dang_tien(tien_nhan_dao_han)}**
        - Số tiền cần:
          **{dinh_dang_tien(so_tien_can)}**
        - Số tiền còn dư:
          **{dinh_dang_tien(tien_du)}**

        Như vậy khách hàng vừa nhận đủ 500 triệu,
        vừa giữ được toàn bộ tiền lãi kỳ hạn.
        """
    )

else:

    st.error(
        "Khoản tiền gửi không đủ để đáp ứng nhu cầu 500 triệu."
    )


# =========================================================
# SO SÁNH VỚI PHƯƠNG ÁN VAY
# =========================================================

st.markdown("### 💡 So sánh với phương án vay")

st.write(
    f"""
    Lãi suất vay: **{lai_suat_vay_de:.1f}%/năm**

    Lãi suất tiền gửi: **{lai_suat_co_ky_han_de:.1f}%/năm**

    Vì:

    **8%/năm > 5%/năm**

    nên nếu khách hàng đã có sẵn 500 triệu trong khoản tiền gửi
    và có thể chờ đến ngày đáo hạn thì **không nên vay 500 triệu
    để thay thế cho khoản tiền gửi này**.
    """
)

st.success(
    """
    🎯 **KẾT LUẬN TƯ VẤN:**

    Nên giữ khoản tiền gửi đến ngày 23/11/2026,
    nhận tiền gốc và lãi, sau đó sử dụng 500 triệu vào ngày 26/11.

    Cách này giúp khách hàng giữ được tiền lãi tiền gửi
    và không phải chịu thêm chi phí lãi vay 8%/năm.
    """
)
