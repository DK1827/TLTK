# =========================================================
# CHỌN TRƯỜNG HỢP NGHIỆP VỤ
# =========================================================

st.divider()

st.header("📝 XÁC ĐỊNH TRƯỜNG HỢP TRONG ĐỀ")

st.info(
    """
    ☑️ Hãy tích vào những trường hợp xuất hiện trong đề bài.
    
    Ứng dụng sẽ chỉ hiển thị phần thông tin và tính toán
    tương ứng với trường hợp được chọn.
    """
)

# =========================================================
# NHÓM 1 - TÌNH HUỐNG RÚT TIỀN
# =========================================================

st.subheader("🏦 1. Trường hợp rút tiền")

col1, col2 = st.columns(2)

with col1:
    rut_dung_han = st.checkbox(
        "☑️ Khách hàng rút đúng hạn"
    )

    rut_truoc_han = st.checkbox(
        "☑️ Khách hàng rút trước hạn"
    )

with col2:
    rut_sau_han = st.checkbox(
        "☑️ Khách hàng rút sau ngày đáo hạn"
    )

    khong_rut_den_han = st.checkbox(
        "☑️ Không rút khi đến hạn / tự động gia hạn"
    )


# =========================================================
# NHÓM 2 - PHƯƠNG THỨC NHẬN LÃI
# =========================================================

st.subheader("💰 2. Phương thức nhận lãi")

nhan_lai_truoc = st.checkbox(
    "☑️ Nhận lãi trước"
)

nhan_lai_hang_thang = st.checkbox(
    "☑️ Nhận lãi hàng tháng"
)

nhan_lai_cuoi_ky = st.checkbox(
    "☑️ Nhận lãi cuối kỳ"
)


# =========================================================
# NHÓM 3 - NHU CẦU VỐN
# =========================================================

st.subheader("💵 3. Nhu cầu sử dụng tiền")

co_nhu_cau_tien = st.checkbox(
    "☑️ Khách hàng cần tiền trước/sau ngày đáo hạn"
)

co_vay_cam_co = st.checkbox(
    "☑️ Khách hàng xem xét vay cầm cố sổ tiết kiệm"
)


# =========================================================
# KIỂM TRA LỰA CHỌN
# =========================================================

st.divider()

st.subheader("📋 Tình huống đã chọn")

cac_truong_hop = []

if rut_dung_han:
    cac_truong_hop.append("Rút đúng hạn")

if rut_truoc_han:
    cac_truong_hop.append("Rút trước hạn")

if rut_sau_han:
    cac_truong_hop.append("Rút sau ngày đáo hạn")

if khong_rut_den_han:
    cac_truong_hop.append("Không rút đến hạn / tự động gia hạn")

if nhan_lai_truoc:
    cac_truong_hop.append("Nhận lãi trước")

if nhan_lai_hang_thang:
    cac_truong_hop.append("Nhận lãi hàng tháng")

if nhan_lai_cuoi_ky:
    cac_truong_hop.append("Nhận lãi cuối kỳ")

if co_nhu_cau_tien:
    cac_truong_hop.append("Có nhu cầu sử dụng tiền")

if co_vay_cam_co:
    cac_truong_hop.append("Vay cầm cố sổ tiết kiệm")


if len(cac_truong_hop) == 0:

    st.warning(
        "⚠️ Chưa chọn trường hợp nào. "
        "Hãy tích ☑️ vào trường hợp xuất hiện trong đề."
    )

else:

    for i, truong_hop in enumerate(cac_truong_hop, 1):
        st.write(f"**{i}. {truong_hop}**")


# =========================================================
# NHẬP THÔNG TIN BỔ SUNG KHI CÓ TRONG ĐỀ
# =========================================================

if rut_truoc_han:

    st.divider()
    st.subheader("📅 Thông tin rút trước hạn")

    ngay_rut_truoc = st.date_input(
        "Ngày khách hàng rút tiền",
        value=ngay_gui
    )

    if ngay_rut_truoc >= ngay_dao_han_ban_dau:

        st.warning(
            "⚠️ Ngày rút đang lớn hơn hoặc bằng ngày đáo hạn. "
            "Hãy kiểm tra lại."
        )

    else:

        so_ngay_truoc = (
            ngay_rut_truoc - ngay_gui
        ).days

        lai_truoc_han = tinh_lai(
            so_tien_gui,
            lai_suat_khong_ky_han,
            so_ngay_truoc
        )

        tong_truoc_han = (
            so_tien_gui + lai_truoc_han
        )

        st.success("✅ Đây là trường hợp rút trước hạn.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "⏱️ Số ngày gửi",
                f"{so_ngay_truoc} ngày"
            )

        with col2:
            st.metric(
                "💵 Tiền lãi",
                dinh_dang_tien(lai_truoc_han)
            )

        with col3:
            st.metric(
                "🏦 Tổng tiền nhận",
                dinh_dang_tien(tong_truoc_han)
            )

        st.info(
            f"""
            **Lãi suất áp dụng:** 
            {lai_suat_khong_ky_han:.2f}%/năm
            
            **Công thức:**
            
            Tiền lãi = Tiền gốc × Lãi suất × Số ngày / 365
            """
        )


# =========================================================
# RÚT ĐÚNG HẠN
# =========================================================

if rut_dung_han:

    st.divider()
    st.subheader("📅 Trường hợp rút đúng hạn")

    lai_dung_han = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        (ngay_dao_han_ban_dau - ngay_gui).days
    )

    tong_dung_han = (
        so_tien_gui + lai_dung_han
    )

    so_ngay_dung_han = (
        ngay_dao_han_ban_dau - ngay_gui
    ).days

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⏱️ Số ngày gửi",
            f"{so_ngay_dung_han} ngày"
        )

    with col2:
        st.metric(
            "💵 Tiền lãi",
            dinh_dang_tien(lai_dung_han)
        )

    with col3:
        st.metric(
            "🏦 Tổng tiền nhận",
            dinh_dang_tien(tong_dung_han)
        )

    st.success(
        f"""
        ✅ Khách hàng rút đúng ngày đáo hạn.
        
        Lãi suất áp dụng: 
        **{lai_suat_co_ky_han:.2f}%/năm**
        """
    )


# =========================================================
# NHẬN LÃI
# =========================================================

if nhan_lai_truoc:

    st.divider()
    st.subheader("💳 Trường hợp nhận lãi trước")

    st.info(
        """
        Khi chọn **nhận lãi trước**, tiền lãi được trả
        cho khách hàng ngay từ đầu kỳ.
        
        Tiền gốc tiếp tục được duy trì trong sổ tiết kiệm.
        """
    )

    lai_du_kien = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        (ngay_dao_han_ban_dau - ngay_gui).days
    )

    st.metric(
        "💵 Tiền lãi dự kiến nhận trước",
        dinh_dang_tien(lai_du_kien)
    )


if nhan_lai_hang_thang:

    st.divider()
    st.subheader("💳 Trường hợp nhận lãi hàng tháng")

    lai_du_kien = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        (ngay_dao_han_ban_dau - ngay_gui).days
    )

    if ky_han > 0:
        lai_moi_thang = lai_du_kien / ky_han
    else:
        lai_moi_thang = 0

    st.metric(
        "💵 Tiền lãi dự kiến mỗi tháng",
        dinh_dang_tien(lai_moi_thang)
    )

    st.info(
        """
        Tiền lãi được trả định kỳ cho khách hàng.
        Tiền gốc không cộng vào tiền gốc của kỳ sau.
        """
    )


if nhan_lai_cuoi_ky:

    st.divider()
    st.subheader("💳 Trường hợp nhận lãi cuối kỳ")

    lai_du_kien = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        (ngay_dao_han_ban_dau - ngay_gui).days
    )

    tong_du_kien = (
        so_tien_gui + lai_du_kien
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi cuối kỳ",
            dinh_dang_tien(lai_du_kien)
        )

    with col2:
        st.metric(
            "🏦 Gốc + lãi",
            dinh_dang_tien(tong_du_kien)
        )

    st.info(
        """
        Tiền lãi được thanh toán khi đến ngày đáo hạn.
        Nếu tiếp tục gia hạn, tiền lãi có thể được nhập
        vào tiền gốc của kỳ tiếp theo.
        """
    )


# =========================================================
# KHÔNG RÚT ĐẾN HẠN / GIA HẠN
# =========================================================

if khong_rut_den_han:

    st.divider()
    st.subheader("🔄 Trường hợp tự động gia hạn")

    st.info(
        """
        ☑️ Khách hàng không rút tiền khi đến ngày đáo hạn.
        
        Sổ tiết kiệm sẽ tiếp tục được gia hạn theo kỳ hạn
        đã đăng ký.
        """
    )

    so_ky = st.number_input(
        "Số kỳ muốn mô phỏng",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    tien_goc_gia_han = so_tien_gui

    bang_gia_han = []

    for ky in range(1, so_ky + 1):

        ngay_bd = (
            ngay_gui
            if ky == 1
            else ngay_bd + relativedelta(months=ky_han)
        )

        ngay_kt = (
            ngay_gui + relativedelta(months=ky_han)
            if ky == 1
            else ngay_bd + relativedelta(months=ky_han)
        )

        so_ngay_ky = (
            ngay_kt - ngay_bd
        ).days

        lai_ky = tinh_lai(
            tien_goc_gia_han,
            lai_suat_co_ky_han,
            so_ngay_ky
        )

        goc_cu = tien_goc_gia_han

        if nhan_lai_cuoi_ky:
            tien_goc_gia_han += lai_ky

        bang_gia_han.append(
            {
                "Kỳ": ky,
                "Ngày bắt đầu": ngay_bd.strftime("%d/%m/%Y"),
                "Ngày kết thúc": ngay_kt.strftime("%d/%m/%Y"),
                "Tiền gốc đầu kỳ": round(goc_cu),
                "Tiền lãi": round(lai_ky),
                "Tiền gốc sau gia hạn": round(tien_goc_gia_han)
            }
        )

    df_gia_han = pd.DataFrame(bang_gia_han)

    st.dataframe(
        df_gia_han,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "🏦 Giá trị sau gia hạn",
        dinh_dang_tien(tien_goc_gia_han)
    )


# =========================================================
# NHU CẦU TIỀN
# =========================================================

if co_nhu_cau_tien:

    st.divider()
    st.subheader("💰 Phân tích nhu cầu sử dụng tiền")

    ngay_can_tien = st.date_input(
        "📅 Ngày khách hàng cần tiền",
        value=ngay_dao_han_ban_dau
    )

    so_tien_can = st.number_input(
        "💵 Số tiền khách hàng cần (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    if ngay_can_tien < ngay_dao_han_ban_dau:

        st.warning(
            """
            ⚠️ Khách hàng cần tiền trước ngày đáo hạn.
            
            Có thể cân nhắc:
            - Rút trước hạn
            - Vay cầm cố sổ tiết kiệm
            """
        )

    elif ngay_can_tien == ngay_dao_han_ban_dau:

        st.success(
            "✅ Khách hàng cần tiền đúng ngày đáo hạn."
        )

    else:

        st.success(
            """
            ✅ Khách hàng cần tiền sau ngày đáo hạn.
            
            Có thể giữ tiền đến đáo hạn rồi sử dụng.
            """
        )


# =========================================================
# VAY CẦM CỐ SỔ TIẾT KIỆM
# =========================================================

if co_vay_cam_co:

    st.divider()
    st.subheader("🏦 Tính khoản vay cầm cố sổ tiết kiệm")

    so_tien_vay = st.number_input(
        "💰 Số tiền muốn vay (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    lai_suat_vay = st.number_input(
        "📈 Lãi suất vay (%/năm)",
        min_value=0.0,
        value=8.0,
        step=0.1,
        format="%.2f"
    )

    so_ngay_vay = st.number_input(
        "📅 Số ngày vay",
        min_value=1,
        value=3,
        step=1
    )

    lai_vay = (
        so_tien_vay
        * lai_suat_vay / 100
        * so_ngay_vay
        / 365
    )

    tong_tra = (
        so_tien_vay + lai_vay
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi vay",
            dinh_dang_tien(lai_vay)
        )

    with col2:
        st.metric(
            "🏦 Tổng tiền phải trả",
            dinh_dang_tien(tong_tra)
        )

    st.info(
        f"""
        **Công thức:**
        
        Tiền lãi vay = Tiền vay × Lãi suất vay × Số ngày / 365
        
        **Lãi suất vay:** {lai_suat_vay:.2f}%/năm
        """
    )


# =========================================================
# TỔNG KẾT
# =========================================================

st.divider()

st.subheader("🎯 TỔNG KẾT TRƯỜNG HỢP")

if len(cac_truong_hop) == 0:

    st.warning(
        "Chưa có trường hợp nào được chọn."
    )

else:

    st.success(
        f"Đã chọn **{len(cac_truong_hop)} trường hợp**."
    )

    for truong_hop in cac_truong_hop:
        st.write(f"☑️ {truong_hop}")


# =========================================================
# CHÂN TRANG
# =========================================================

st.divider()

st.caption(
    "🏦 Ứng dụng tính lãi tiền gửi tiết kiệm - Streamlit"
)

st.caption(
    "📚 Công cụ hỗ trợ xử lý các trường hợp trong bài tập"
)
