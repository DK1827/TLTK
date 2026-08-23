import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi tiết kiệm ngân hàng",
    page_icon="🏦",
    layout="centered"
)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🏦 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")

st.markdown(
    """
    Ứng dụng hỗ trợ tính tiền lãi tiền gửi tiết kiệm theo:
    
    - Lãi suất có kỳ hạn
    - Lãi suất không kỳ hạn
    - Kỳ hạn gửi
    - Ngày gửi và ngày rút
    - Phương thức nhận lãi
    """
)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================================================
# HÀM TÍNH LÃI
# =========================================================

def tinh_lai(so_tien, lai_suat_nam, so_ngay):
    """
    Tính lãi theo số ngày thực tế.
    
    Công thức:
    Tiền lãi = Tiền gốc × Lãi suất năm × Số ngày / 365
    """

    lai = so_tien * (lai_suat_nam / 100) * so_ngay / 365

    return lai


# =========================================================
# HÀM TÍNH NGÀY ĐÁO HẠN
# =========================================================

def tinh_ngay_dao_han(ngay_bat_dau, ky_han_thang):
    return ngay_bat_dau + relativedelta(months=ky_han_thang)


# =========================================================
# NHẬP THÔNG TIN KHÁCH HÀNG
# =========================================================

st.header("📋 Thông tin tiền gửi")


so_tien_gui = st.number_input(
    "💰 Số tiền khách hàng gửi (VNĐ)",
    min_value=0.0,
    value=500_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)


lai_suat_co_ky_han = st.number_input(
    "📈 Lãi suất có kỳ hạn (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)


lai_suat_khong_ky_han = st.number_input(
    "📉 Lãi suất không kỳ hạn (%/năm)",
    min_value=0.0,
    value=0.2,
    step=0.01,
    format="%.2f"
)


# =========================================================
# NGÀY GỬI
# =========================================================

ngay_gui = st.date_input(
    "📅 Ngày gửi tiền",
    value=date.today()
)


# =========================================================
# KỲ HẠN
# =========================================================

ky_han = st.selectbox(
    "⏳ Kỳ hạn gửi tiền",
    options=[
        1,
        3,
        6,
        9,
        12,
        18,
        24,
        36
    ],
    format_func=lambda x: f"{x} tháng"
)


# =========================================================
# NGÀY ĐÁO HẠN DỰ KIẾN
# =========================================================

ngay_dao_han_ban_dau = tinh_ngay_dao_han(
    ngay_gui,
    ky_han
)

st.info(
    f"📅 Ngày đáo hạn dự kiến: "
    f"**{ngay_dao_han_ban_dau.strftime('%d/%m/%Y')}**"
)


# =========================================================
# NGÀY RÚT TIỀN
# =========================================================

ngay_rut = st.date_input(
    "💵 Ngày khách hàng rút tiền",
    value=ngay_dao_han_ban_dau
)


# =========================================================
# PHƯƠNG THỨC NHẬN LÃI
# =========================================================

phuong_thuc_lai = st.selectbox(
    "💳 Phương thức nhận tiền lãi",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng tháng",
        "Nhận lãi cuối kỳ"
    ]
)


# =========================================================
# THÔNG TIN QUY ƯỚC
# =========================================================

with st.expander("ℹ️ Quy ước tính toán"):

    st.write(
        """
        **1. Rút trước hạn:**
        
        Nếu khách hàng rút trước ngày đáo hạn, toàn bộ số tiền
        được tính theo lãi suất không kỳ hạn.
        
        **2. Số ngày tính lãi:**
        
        Lãi được tính từ ngày gửi đến **trước ngày đáo hạn
        hoặc trước ngày khách hàng rút tiền**.
        
        Ví dụ: gửi ngày 01/01 và đáo hạn ngày 01/07 thì số ngày
        tính lãi là khoảng thời gian từ 01/01 đến 01/07,
        tương ứng `ngày đáo hạn - ngày gửi`.
        
        **3. Tự động gia hạn:**
        
        Nếu khách hàng không rút khi đến hạn, tiền gửi sẽ
        tự động gia hạn với đúng kỳ hạn ban đầu.
        
        **4. Nhận lãi cuối kỳ:**
        
        Khi tự động gia hạn, tiền lãi của kỳ trước được nhập
        vào tiền gốc để tiếp tục sinh lãi.
        
        **5. Nhận lãi trước/hàng tháng:**
        
        Tiền lãi được xem là đã trả cho khách hàng, tiền gốc
        tiếp tục được gia hạn.
        """
    )


# =========================================================
# NÚT TÍNH TOÁN
# =========================================================

st.divider()

tinh_toan = st.button(
    "🧮 TÍNH TOÁN",
    type="primary",
    use_container_width=True
)


# =========================================================
# TÍNH TOÁN
# =========================================================

if tinh_toan:

    # -----------------------------------------------------
    # KIỂM TRA DỮ LIỆU
    # -----------------------------------------------------

    if so_tien_gui <= 0:

        st.error("❌ Số tiền gửi phải lớn hơn 0 VNĐ.")

    elif ngay_rut < ngay_gui:

        st.error(
            "❌ Ngày rút tiền phải lớn hơn hoặc bằng ngày gửi tiền."
        )

    else:

        # =================================================
        # TRƯỜNG HỢP 1: RÚT TRƯỚC HẠN
        # =================================================

        if ngay_rut < ngay_dao_han_ban_dau:

            so_ngay = (ngay_rut - ngay_gui).days

            lai = tinh_lai(
                so_tien_gui,
                lai_suat_khong_ky_han,
                so_ngay
            )

            tong_tien = so_tien_gui + lai

            st.warning(
                "⚠️ Khách hàng rút trước hạn. "
                "Toàn bộ thời gian gửi được áp dụng lãi suất "
                "không kỳ hạn."
            )

            # -------------------------------------------------
            # KẾT QUẢ
            # -------------------------------------------------

            st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "💰 Tiền gốc",
                    dinh_dang_tien(so_tien_gui)
                )

                st.metric(
                    "⏱️ Số ngày gửi",
                    f"{so_ngay} ngày"
                )

            with col2:

                st.metric(
                    "💵 Tiền lãi",
                    dinh_dang_tien(lai)
                )

                st.metric(
                    "🏦 Tổng tiền nhận",
                    dinh_dang_tien(tong_tien)
                )

            st.info(
                f"""
                **Lãi suất áp dụng:** {lai_suat_khong_ky_han:.2f}%/năm  
                **Loại lãi suất:** Không kỳ hạn  
                **Phương thức nhận lãi:** {phuong_thuc_lai}
                """
            )

        # =================================================
        # TRƯỜNG HỢP 2: RÚT ĐÚNG HẠN
        # =================================================

        elif ngay_rut == ngay_dao_han_ban_dau:

            so_ngay = (
                ngay_dao_han_ban_dau - ngay_gui
            ).days

            lai = tinh_lai(
                so_tien_gui,
                lai_suat_co_ky_han,
                so_ngay
            )

            # -------------------------------------------------
            # NHẬN LÃI TRƯỚC
            # -------------------------------------------------

            if phuong_thuc_lai == "Nhận lãi trước":

                tien_lai_da_nhan = lai

                tien_goc_nhan = so_tien_gui

                tong_tien = tien_goc_nhan + tien_lai_da_nhan

                ten_phuong_thuc = "Nhận lãi trước"

            # -------------------------------------------------
            # NHẬN LÃI HÀNG THÁNG
            # -------------------------------------------------

            elif phuong_thuc_lai == "Nhận lãi hàng tháng":

                so_thang = ky_han

                lai_hang_thang = lai / so_thang

                tien_lai_da_nhan = lai

                tien_goc_nhan = so_tien_gui

                tong_tien = tien_goc_nhan + tien_lai_da_nhan

                ten_phuong_thuc = "Nhận lãi hàng tháng"

            # -------------------------------------------------
            # NHẬN LÃI CUỐI KỲ
            # -------------------------------------------------

            else:

                tien_lai_da_nhan = lai

                tien_goc_nhan = so_tien_gui

                tong_tien = so_tien_gui + lai

                ten_phuong_thuc = "Nhận lãi cuối kỳ"

            # -------------------------------------------------
            # HIỂN THỊ KẾT QUẢ
            # -------------------------------------------------

            st.success(
                "✅ Khách hàng rút đúng ngày đáo hạn."
            )

            st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "💰 Tiền gốc",
                    dinh_dang_tien(tien_goc_nhan)
                )

                st.metric(
                    "⏱️ Số ngày gửi",
                    f"{so_ngay} ngày"
                )

            with col2:

                st.metric(
                    "💵 Tổng tiền lãi",
                    dinh_dang_tien(tien_lai_da_nhan)
                )

                st.metric(
                    "🏦 Tổng tiền khách hàng nhận",
                    dinh_dang_tien(tong_tien)
                )

            # -------------------------------------------------
            # CHI TIẾT
            # -------------------------------------------------

            st.info(
                f"""
                **Lãi suất áp dụng:** {lai_suat_co_ky_han:.2f}%/năm  
                **Loại lãi suất:** Có kỳ hạn  
                **Kỳ hạn:** {ky_han} tháng  
                **Phương thức nhận lãi:** {ten_phuong_thuc}
                """
            )

            if phuong_thuc_lai == "Nhận lãi hàng tháng":

                st.write(
                    f"💳 Tiền lãi nhận mỗi tháng: "
                    f"**{dinh_dang_tien(lai_hang_thang)}**"
                )

        # =================================================
        # TRƯỜNG HỢP 3: RÚT SAU NGÀY ĐÁO HẠN
        # =================================================

        else:

            st.warning(
                "🔄 Khách hàng không rút khi đến hạn. "
                "Tiền gửi được tự động gia hạn theo đúng kỳ hạn."
            )

            # -------------------------------------------------
            # BIẾN BAN ĐẦU
            # -------------------------------------------------

            ngay_bat_dau_ky = ngay_gui

            tien_goc = so_tien_gui

            tong_lai_da_nhan = 0

            so_ky_gia_han = 0

            danh_sach_ky = []

            # Dùng để lưu số tiền lãi của kỳ hiện tại
            lai_ky_hien_tai = 0

            # -------------------------------------------------
            # TÍNH TỪNG KỲ
            # -------------------------------------------------

            while True:

                ngay_dao_han = tinh_ngay_dao_han(
                    ngay_bat_dau_ky,
                    ky_han
                )

                # Nếu ngày rút nằm trong kỳ hiện tại
                if ngay_rut <= ngay_dao_han:

                    so_ngay_ky = (
                        ngay_rut - ngay_bat_dau_ky
                    ).days

                    # Nếu đúng ngày đáo hạn
                    if ngay_rut == ngay_dao_han:

                        so_ngay_ky = (
                            ngay_dao_han - ngay_bat_dau_ky
                        ).days

                        lai_ky_hien_tai = tinh_lai(
                            tien_goc,
                            lai_suat_co_ky_han,
                            so_ngay_ky
                        )

                        danh_sach_ky.append(
                            {
                                "Kỳ": so_ky_gia_han + 1,
                                "Ngày bắt đầu": ngay_bat_dau_ky,
                                "Ngày kết thúc": ngay_dao_han,
                                "Số ngày": so_ngay_ky,
                                "Tiền gốc": tien_goc,
                                "Tiền lãi": lai_ky_hien_tai
                            }
                        )

                        # -------------------------------------
                        # NHẬN LÃI CUỐI KỲ
                        # -------------------------------------

                        if phuong_thuc_lai == "Nhận lãi cuối kỳ":

                            tong_lai_da_nhan += lai_ky_hien_tai

                            tien_goc = (
                                tien_goc + lai_ky_hien_tai
                            )

                        else:

                            tong_lai_da_nhan += lai_ky_hien_tai

                        break

                    # Rút trước ngày đáo hạn của kỳ hiện tại
                    else:

                        lai_ky_hien_tai = tinh_lai(
                            tien_goc,
                            lai_suat_khong_ky_han,
                            so_ngay_ky
                        )

                        danh_sach_ky.append(
                            {
                                "Kỳ": so_ky_gia_han + 1,
                                "Ngày bắt đầu": ngay_bat_dau_ky,
                                "Ngày kết thúc": ngay_rut,
                                "Số ngày": so_ngay_ky,
                                "Tiền gốc": tien_goc,
                                "Tiền lãi": lai_ky_hien_tai
                            }
                        )

                        tong_lai_da_nhan += lai_ky_hien_tai

                        break

                # ---------------------------------------------
                # ĐÃ HẾT MỘT KỲ VÀ TỰ ĐỘNG GIA HẠN
                # ---------------------------------------------

                else:

                    so_ngay_ky = (
                        ngay_dao_han - ngay_bat_dau_ky
                    ).days

                    lai_ky_hien_tai = tinh_lai(
                        tien_goc,
                        lai_suat_co_ky_han,
                        so_ngay_ky
                    )

                    danh_sach_ky.append(
                        {
                            "Kỳ": so_ky_gia_han + 1,
                            "Ngày bắt đầu": ngay_bat_dau_ky,
                            "Ngày kết thúc": ngay_dao_han,
                            "Số ngày": so_ngay_ky,
                            "Tiền gốc": tien_goc,
                            "Tiền lãi": lai_ky_hien_tai
                        }
                    )

                    # =========================================
                    # NHẬN LÃI CUỐI KỲ
                    # =========================================

                    if phuong_thuc_lai == "Nhận lãi cuối kỳ":

                        # Lãi nhập gốc khi gia hạn
                        tien_goc = (
                            tien_goc + lai_ky_hien_tai
                        )

                        tong_lai_da_nhan += lai_ky_hien_tai

                    # =========================================
                    # NHẬN LÃI TRƯỚC / HÀNG THÁNG
                    # =========================================

                    else:

                        # Lãi được trả cho khách hàng,
                        # gốc giữ nguyên để gia hạn
                        tong_lai_da_nhan += lai_ky_hien_tai

                    so_ky_gia_han += 1

                    ngay_bat_dau_ky = ngay_dao_han

            # =================================================
            # TỔNG TIỀN NHẬN
            # =================================================

            tong_tien_nhan = tien_goc

            # =================================================
            # HIỂN THỊ KẾT QUẢ
            # =================================================

            st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "💰 Tiền gốc cuối cùng",
                    dinh_dang_tien(tien_goc)
                )

                st.metric(
                    "🔄 Số lần gia hạn",
                    f"{so_ky_gia_han} lần"
                )

            with col2:

                st.metric(
                    "💵 Tổng tiền lãi",
                    dinh_dang_tien(tong_lai_da_nhan)
                )

                # Nếu lãi cuối kỳ, tiền gốc đã bao gồm lãi
                if phuong_thuc_lai == "Nhận lãi cuối kỳ":

                    tong_tien_khach_nhan = tien_goc

                else:

                    tong_tien_khach_nhan = (
                        so_tien_gui + tong_lai_da_nhan
                    )

                st.metric(
                    "🏦 Tổng giá trị khách hàng nhận",
                    dinh_dang_tien(tong_tien_khach_nhan)
                )

            # =================================================
            # THÔNG TIN PHƯƠNG THỨC NHẬN LÃI
            # =================================================

            if phuong_thuc_lai == "Nhận lãi cuối kỳ":

                st.info(
                    """
                    💰 **Lãi cuối kỳ:** Tiền lãi của mỗi kỳ được
                    nhập vào tiền gốc khi ngân hàng tự động gia hạn.
                    Vì vậy các kỳ sau sẽ tiếp tục phát sinh lãi
                    trên cả phần gốc và lãi của kỳ trước.
                    """
                )

            elif phuong_thuc_lai == "Nhận lãi hàng tháng":

                st.info(
                    """
                    💳 **Lãi hàng tháng:** Tiền lãi được trả cho
                    khách hàng theo từng tháng. Tiền gốc tiếp tục
                    được tự động gia hạn khi đến hạn.
                    """
                )

            else:

                st.info(
                    """
                    💵 **Lãi trước:** Tiền lãi của từng kỳ được
                    trả ngay từ đầu kỳ. Tiền gốc tiếp tục được
                    tự động gia hạn.
                    """
                )

            # =================================================
            # BẢNG CHI TIẾT CÁC KỲ
            # =================================================

            st.subheader("📑 Chi tiết các kỳ gửi")

            for ky in danh_sach_ky:

                st.write(
                    f"### Kỳ {ky['Kỳ']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"📅 Bắt đầu: "
                        f"**{ky['Ngày bắt đầu'].strftime('%d/%m/%Y')}**"
                    )

                with col2:
                    st.write(
                        f"📅 Kết thúc: "
                        f"**{ky['Ngày kết thúc'].strftime('%d/%m/%Y')}**"
                    )

                with col3:
                    st.write(
                        f"⏱️ Số ngày: **{ky['Số ngày']} ngày**"
                    )

                st.write(
                    f"💰 Gốc đầu kỳ: "
                    f"**{dinh_dang_tien(ky['Tiền gốc'])}**"
                )

                st.write(
                    f"💵 Lãi kỳ này: "
                    f"**{dinh_dang_tien(ky['Tiền lãi'])}**"
                )

                st.divider()


# =========================================================
# CHÂN TRANG
# =========================================================

st.caption(
    "🏦 Ứng dụng tính lãi tiền gửi tiết kiệm - Streamlit"
)
