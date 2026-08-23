# =========================================================
# 4. CHỌN KHOẢNG THỜI GIAN TÍNH LÃI
# =========================================================

st.subheader("📅 4. Chọn khoảng thời gian tính lãi")

chon_khoang_ngay = st.checkbox(
    "☑️ Tính lãi từ ngày ... đến ngày ...",
    key="chon_khoang_ngay_case"
)

if chon_khoang_ngay:

    col1, col2 = st.columns(2)

    with col1:
        ngay_bat_dau_tinh = st.date_input(
            "📅 Từ ngày",
            value=ngay_gui,
            key="ngay_bat_dau_tinh_case"
        )

    with col2:
        ngay_ket_thuc_tinh = st.date_input(
            "📅 Đến ngày",
            value=ngay_dao_han_ban_dau,
            key="ngay_ket_thuc_tinh_case"
        )

    # ---------------------------------------------------------
    # CHỌN LOẠI LÃI SUẤT
    # ---------------------------------------------------------

    loai_lai_khoang_ngay = st.radio(
        "📈 Loại lãi suất áp dụng",
        [
            "Lãi suất có kỳ hạn",
            "Lãi suất không kỳ hạn"
        ],
        horizontal=True,
        key="loai_lai_khoang_ngay_case"
    )

    if ngay_ket_thuc_tinh < ngay_bat_dau_tinh:

        st.error(
            "❌ Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu."
        )

    else:

        so_ngay_khoang = (
            ngay_ket_thuc_tinh - ngay_bat_dau_tinh
        ).days

        if loai_lai_khoang_ngay == "Lãi suất có kỳ hạn":
            lai_suat_ap_dung = lai_suat_co_ky_han
        else:
            lai_suat_ap_dung = lai_suat_khong_ky_han

        lai_khoang_ngay = tinh_lai(
            so_tien_gui,
            lai_suat_ap_dung,
            so_ngay_khoang
        )

        tong_khoang_ngay = (
            so_tien_gui + lai_khoang_ngay
        )

        # -----------------------------------------------------
        # HIỂN THỊ KẾT QUẢ
        # -----------------------------------------------------

        st.success(
            f"""
            ✅ Đã chọn khoảng thời gian:

            **{ngay_bat_dau_tinh.strftime('%d/%m/%Y')}**
            → 
            **{ngay_ket_thuc_tinh.strftime('%d/%m/%Y')}**
            """
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "⏱️ Số ngày",
                f"{so_ngay_khoang} ngày"
            )

        with col2:
            st.metric(
                "💵 Tiền lãi",
                dinh_dang_tien(lai_khoang_ngay)
            )

        with col3:
            st.metric(
                "🏦 Gốc + lãi",
                dinh_dang_tien(tong_khoang_ngay)
            )

        st.info(
            f"""
            **📅 Khoảng thời gian:**
            {ngay_bat_dau_tinh.strftime('%d/%m/%Y')}
            → {ngay_ket_thuc_tinh.strftime('%d/%m/%Y')}

            **⏱️ Số ngày:** {so_ngay_khoang} ngày

            **📈 Lãi suất áp dụng:**
            {lai_suat_ap_dung:.2f}%/năm

            **🧮 Công thức:**

            Tiền lãi = Tiền gốc × Lãi suất × Số ngày / 365
            """
        )
