import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd


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

    - 💰 Số tiền gửi
    - 📈 Lãi suất có kỳ hạn
    - 📉 Lãi suất không kỳ hạn
    - ⏳ Kỳ hạn gửi
    - 📅 Ngày gửi và ngày rút
    - 📅 Chọn khoảng thời gian từ ngày đến ngày
    - 💳 Phương thức nhận lãi
    - 🔄 Tự động gia hạn
    - 📝 Giải bài tập theo yêu cầu
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
    Công thức:
    Tiền lãi = Tiền gốc × Lãi suất năm × Số ngày / 365
    """

    lai = (
        so_tien
        * (lai_suat_nam / 100)
        * so_ngay
        / 365
    )

    return lai


# =========================================================
# HÀM TÍNH NGÀY ĐÁO HẠN
# =========================================================

def tinh_ngay_dao_han(ngay_bat_dau, ky_han_thang):
    return ngay_bat_dau + relativedelta(
        months=ky_han_thang
    )


# =========================================================
# HÀM TÍNH LÃI CHO BÀI TẬP
# =========================================================

def tinh_lai_bai(
    so_tien,
    lai_suat,
    ngay_bat_dau,
    ngay_ket_thuc
):
    so_ngay = (
        ngay_ket_thuc - ngay_bat_dau
    ).days

    lai = tinh_lai(
        so_tien,
        lai_suat,
        so_ngay
    )

    return so_ngay, lai


# =========================================================
# NHẬP THÔNG TIN KHÁCH HÀNG
# =========================================================

st.header("📋 Thông tin tiền gửi")


# ---------------------------------------------------------
# SỐ TIỀN GỬI
# ---------------------------------------------------------

so_tien_gui = st.number_input(
    "💰 Số tiền khách hàng gửi (VNĐ)",
    min_value=0.0,
    value=500_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)


# ---------------------------------------------------------
# LÃI SUẤT CÓ KỲ HẠN
# ---------------------------------------------------------

lai_suat_co_ky_han = st.number_input(
    "📈 Lãi suất có kỳ hạn (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)


# ---------------------------------------------------------
# LÃI SUẤT KHÔNG KỲ HẠN
# ---------------------------------------------------------

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
    value=date(2026, 8, 23)
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
    index=1,
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
    f"""
    📅 Ngày đáo hạn dự kiến:

    **{ngay_dao_han_ban_dau.strftime('%d/%m/%Y')}**
    """
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
    ],
    index=2
)


# =========================================================
# THÔNG TIN QUY ƯỚC
# =========================================================

with st.expander("ℹ️ Quy ước tính toán"):

    st.write(
        """
        **1. Rút trước hạn:**

        Nếu khách hàng rút trước ngày đáo hạn,
        toàn bộ số tiền được tính theo lãi suất không kỳ hạn.

        **2. Số ngày tính lãi:**

        Lãi được tính theo số ngày thực tế:

        `Tiền lãi = Tiền gốc × Lãi suất năm × Số ngày / 365`

        **3. Tự động gia hạn:**

        Nếu khách hàng không rút khi đến hạn,
        tiền gửi sẽ tự động gia hạn với đúng kỳ hạn ban đầu.

        **4. Nhận lãi cuối kỳ:**

        Tiền lãi của kỳ trước được nhập vào tiền gốc
        để tiếp tục sinh lãi khi gia hạn.

        **5. Nhận lãi trước/hàng tháng:**

        Tiền lãi được trả cho khách hàng,
        tiền gốc tiếp tục được gia hạn.

        **6. Chọn khoảng thời gian:**

        Có thể chọn một khoảng thời gian bất kỳ
        từ ngày bắt đầu đến ngày kết thúc để tính lãi.
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

        st.error(
            "❌ Số tiền gửi phải lớn hơn 0 VNĐ."
        )

    elif ngay_rut < ngay_gui:

        st.error(
            "❌ Ngày rút tiền phải lớn hơn hoặc bằng ngày gửi tiền."
        )

    else:

        # =================================================
        # TRƯỜNG HỢP 1: RÚT TRƯỚC HẠN
        # =================================================

        if ngay_rut < ngay_dao_han_ban_dau:

            so_ngay = (
                ngay_rut - ngay_gui
            ).days

            lai = tinh_lai(
                so_tien_gui,
                lai_suat_khong_ky_han,
                so_ngay
            )

            tong_tien = (
                so_tien_gui + lai
            )

            st.warning(
                """
                ⚠️ Khách hàng rút trước hạn.

                Toàn bộ thời gian gửi được áp dụng
                lãi suất không kỳ hạn.
                """
            )

            # -------------------------------------------------
            # KẾT QUẢ
            # -------------------------------------------------

            st.subheader(
                "📊 KẾT QUẢ TÍNH TOÁN"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "💰 Tiền gốc",
                    dinh_dang_tien(
                        so_tien_gui
                    )
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
                **Lãi suất áp dụng:**
                {lai_suat_khong_ky_han:.2f}%/năm

                **Loại lãi suất:** Không kỳ hạn

                **Phương thức nhận lãi:**
                {phuong_thuc_lai}
                """
            )


        # =================================================
        # TRƯỜNG HỢP 2: RÚT ĐÚNG HẠN
        # =================================================

        elif ngay_rut == ngay_dao_han_ban_dau:

            so_ngay = (
                ngay_dao_han_ban_dau
                - ngay_gui
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

                tong_tien = (
                    tien_goc_nhan
                    + tien_lai_da_nhan
                )

                ten_phuong_thuc = (
                    "Nhận lãi trước"
                )

            # -------------------------------------------------
            # NHẬN LÃI HÀNG THÁNG
            # -------------------------------------------------

            elif phuong_thuc_lai == "Nhận lãi hàng tháng":

                so_thang = ky_han

                lai_hang_thang = (
                    lai / so_thang
                )

                tien_lai_da_nhan = lai

                tien_goc_nhan = so_tien_gui

                tong_tien = (
                    tien_goc_nhan
                    + tien_lai_da_nhan
                )

                ten_phuong_thuc = (
                    "Nhận lãi hàng tháng"
                )

            # -------------------------------------------------
            # NHẬN LÃI CUỐI KỲ
            # -------------------------------------------------

            else:

                tien_lai_da_nhan = lai

                tien_goc_nhan = so_tien_gui

                tong_tien = (
                    so_tien_gui + lai
                )

                ten_phuong_thuc = (
                    "Nhận lãi cuối kỳ"
                )

            # -------------------------------------------------
            # HIỂN THỊ
            # -------------------------------------------------

            st.success(
                "✅ Khách hàng rút đúng ngày đáo hạn."
            )

            st.subheader(
                "📊 KẾT QUẢ TÍNH TOÁN"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "💰 Tiền gốc",
                    dinh_dang_tien(
                        tien_goc_nhan
                    )
                )

                st.metric(
                    "⏱️ Số ngày gửi",
                    f"{so_ngay} ngày"
                )

            with col2:

                st.metric(
                    "💵 Tổng tiền lãi",
                    dinh_dang_tien(
                        tien_lai_da_nhan
                    )
                )

                st.metric(
                    "🏦 Tổng tiền khách hàng nhận",
                    dinh_dang_tien(
                        tong_tien
                    )
                )

            st.info(
                f"""
                **Lãi suất áp dụng:**
                {lai_suat_co_ky_han:.2f}%/năm

                **Loại lãi suất:** Có kỳ hạn

                **Kỳ hạn:** {ky_han} tháng

                **Phương thức nhận lãi:**
                {ten_phuong_thuc}
                """
            )

            if phuong_thuc_lai == "Nhận lãi hàng tháng":

                st.write(
                    f"""
                    💳 Tiền lãi nhận mỗi tháng:

                    **{dinh_dang_tien(lai_hang_thang)}**
                    """
                )


        # =================================================
        # TRƯỜNG HỢP 3: RÚT SAU NGÀY ĐÁO HẠN
        # =================================================

        else:

            st.warning(
                """
                🔄 Khách hàng không rút khi đến hạn.

                Tiền gửi được tự động gia hạn
                theo đúng kỳ hạn.
                """
            )

            # -------------------------------------------------
            # BIẾN BAN ĐẦU
            # -------------------------------------------------

            ngay_bat_dau_ky = ngay_gui

            tien_goc = so_tien_gui

            tong_lai_da_nhan = 0

            so_ky_gia_han = 0

            danh_sach_ky = []

            # -------------------------------------------------
            # TÍNH TỪNG KỲ
            # -------------------------------------------------

            while True:

                ngay_dao_han = tinh_ngay_dao_han(
                    ngay_bat_dau_ky,
                    ky_han
                )

                # ---------------------------------------------
                # NGÀY RÚT NẰM TRONG KỲ HIỆN TẠI
                # ---------------------------------------------

                if ngay_rut <= ngay_dao_han:

                    so_ngay_ky = (
                        ngay_rut
                        - ngay_bat_dau_ky
                    ).days

                    # -----------------------------------------
                    # ĐÚNG NGÀY ĐÁO HẠN
                    # -----------------------------------------

                    if ngay_rut == ngay_dao_han:

                        so_ngay_ky = (
                            ngay_dao_han
                            - ngay_bat_dau_ky
                        ).days

                        lai_ky_hien_tai = tinh_lai(
                            tien_goc,
                            lai_suat_co_ky_han,
                            so_ngay_ky
                        )

                        danh_sach_ky.append(
                            {
                                "Kỳ": so_ky_gia_han + 1,
                                "Ngày bắt đầu":
                                    ngay_bat_dau_ky,
                                "Ngày kết thúc":
                                    ngay_dao_han,
                                "Số ngày":
                                    so_ngay_ky,
                                "Tiền gốc":
                                    tien_goc,
                                "Tiền lãi":
                                    lai_ky_hien_tai
                            }
                        )

                        if (
                            phuong_thuc_lai
                            == "Nhận lãi cuối kỳ"
                        ):

                            tong_lai_da_nhan += (
                                lai_ky_hien_tai
                            )

                            tien_goc = (
                                tien_goc
                                + lai_ky_hien_tai
                            )

                        else:

                            tong_lai_da_nhan += (
                                lai_ky_hien_tai
                            )

                        break

                    # -----------------------------------------
                    # RÚT TRƯỚC ĐÁO HẠN CỦA KỲ HIỆN TẠI
                    # -----------------------------------------

                    else:

                        lai_ky_hien_tai = tinh_lai(
                            tien_goc,
                            lai_suat_khong_ky_han,
                            so_ngay_ky
                        )

                        danh_sach_ky.append(
                            {
                                "Kỳ": so_ky_gia_han + 1,
                                "Ngày bắt đầu":
                                    ngay_bat_dau_ky,
                                "Ngày kết thúc":
                                    ngay_rut,
                                "Số ngày":
                                    so_ngay_ky,
                                "Tiền gốc":
                                    tien_goc,
                                "Tiền lãi":
                                    lai_ky_hien_tai
                            }
                        )

                        tong_lai_da_nhan += (
                            lai_ky_hien_tai
                        )

                        break

                # ---------------------------------------------
                # HẾT MỘT KỲ → GIA HẠN
                # ---------------------------------------------

                else:

                    so_ngay_ky = (
                        ngay_dao_han
                        - ngay_bat_dau_ky
                    ).days

                    lai_ky_hien_tai = tinh_lai(
                        tien_goc,
                        lai_suat_co_ky_han,
                        so_ngay_ky
                    )

                    danh_sach_ky.append(
                        {
                            "Kỳ": so_ky_gia_han + 1,
                            "Ngày bắt đầu":
                                ngay_bat_dau_ky,
                            "Ngày kết thúc":
                                ngay_dao_han,
                            "Số ngày":
                                so_ngay_ky,
                            "Tiền gốc":
                                tien_goc,
                            "Tiền lãi":
                                lai_ky_hien_tai
                        }
                    )

                    # -----------------------------------------
                    # NHẬN LÃI CUỐI KỲ
                    # -----------------------------------------

                    if (
                        phuong_thuc_lai
                        == "Nhận lãi cuối kỳ"
                    ):

                        tien_goc = (
                            tien_goc
                            + lai_ky_hien_tai
                        )

                        tong_lai_da_nhan += (
                            lai_ky_hien_tai
                        )

                    # -----------------------------------------
                    # NHẬN LÃI TRƯỚC/HÀNG THÁNG
                    # -----------------------------------------

                    else:

                        tong_lai_da_nhan += (
                            lai_ky_hien_tai
                        )

                    so_ky_gia_han += 1

                    ngay_bat_dau_ky = (
                        ngay_dao_han
                    )

            # =================================================
            # TỔNG TIỀN NHẬN
            # =================================================

            tong_tien_nhan = tien_goc

            # =================================================
            # HIỂN THỊ KẾT QUẢ
            # =================================================

            st.subheader(
                "📊 KẾT QUẢ TÍNH TOÁN"
            )

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
                    dinh_dang_tien(
                        tong_lai_da_nhan
                    )
                )

                if (
                    phuong_thuc_lai
                    == "Nhận lãi cuối kỳ"
                ):

                    tong_tien_khach_nhan = (
                        tien_goc
                    )

                else:

                    tong_tien_khach_nhan = (
                        so_tien_gui
                        + tong_lai_da_nhan
                    )

                st.metric(
                    "🏦 Tổng giá trị khách hàng nhận",
                    dinh_dang_tien(
                        tong_tien_khach_nhan
                    )
                )

            # =================================================
            # THÔNG TIN PHƯƠNG THỨC
            # =================================================

            if (
                phuong_thuc_lai
                == "Nhận lãi cuối kỳ"
            ):

                st.info(
                    """
                    💰 **Lãi cuối kỳ:**

                    Tiền lãi của mỗi kỳ được nhập vào
                    tiền gốc khi ngân hàng tự động gia hạn.
                    """
                )

            elif (
                phuong_thuc_lai
                == "Nhận lãi hàng tháng"
            ):

                st.info(
                    """
                    💳 **Lãi hàng tháng:**

                    Tiền lãi được trả cho khách hàng
                    theo từng tháng.

                    Tiền gốc tiếp tục được gia hạn.
                    """
                )

            else:

                st.info(
                    """
                    💵 **Lãi trước:**

                    Tiền lãi của từng kỳ được trả ngay
                    từ đầu kỳ.

                    Tiền gốc tiếp tục được gia hạn.
                    """
                )

            # =================================================
            # BẢNG CHI TIẾT CÁC KỲ
            # =================================================

            st.subheader(
                "📑 Chi tiết các kỳ gửi"
            )

            for ky in danh_sach_ky:

                st.write(
                    f"### Kỳ {ky['Kỳ']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"""
                        📅 Bắt đầu:

                        **{ky['Ngày bắt đầu'].strftime('%d/%m/%Y')}**
                        """
                    )

                with col2:

                    st.write(
                        f"""
                        📅 Kết thúc:

                        **{ky['Ngày kết thúc'].strftime('%d/%m/%Y')}**
                        """
                    )

                with col3:

                    st.write(
                        f"""
                        ⏱️ Số ngày:

                        **{ky['Số ngày']} ngày**
                        """
                    )

                st.write(
                    f"""
                    💰 Gốc đầu kỳ:

                    **{dinh_dang_tien(ky['Tiền gốc'])}**
                    """
                )

                st.write(
                    f"""
                    💵 Lãi kỳ này:

                    **{dinh_dang_tien(ky['Tiền lãi'])}**
                    """
                )

                st.divider()


# =========================================================
# XỬ LÝ CÁC TRƯỜNG HỢP TRONG ĐỀ BÀI
# =========================================================

st.divider()

st.header("📝 XỬ LÝ TRƯỜNG HỢP TRONG ĐỀ")

st.info(
    """
    **Hướng dẫn:**

    Không có đề bài cố định trong ứng dụng.

    Hãy nhập dữ liệu ở phần **Thông tin tiền gửi** phía trên,
    sau đó tích ☑️ vào đúng trường hợp xuất hiện trong đề.

    Ứng dụng sẽ hiển thị phần xử lý tương ứng.

    Bạn cũng có thể tích ☑️ **Tính lãi từ ngày đến ngày**
    để nhập một khoảng thời gian bất kỳ.
    """
)


# =========================================================
# 1. TRƯỜNG HỢP RÚT TIỀN
# =========================================================

st.subheader("🏦 1. Trường hợp rút tiền")

col1, col2 = st.columns(2)

with col1:

    rut_dung_han = st.checkbox(
        "☑️ Rút đúng hạn",
        key="rut_dung_han_case"
    )

    rut_truoc_han = st.checkbox(
        "☑️ Rút trước hạn",
        key="rut_truoc_han_case"
    )

with col2:

    rut_sau_han = st.checkbox(
        "☑️ Rút sau ngày đáo hạn",
        key="rut_sau_han_case"
    )

    tu_dong_gia_han = st.checkbox(
        "☑️ Không rút khi đến hạn / tự động gia hạn",
        key="tu_dong_gia_han_case"
    )


# =========================================================
# 2. PHƯƠNG THỨC NHẬN LÃI
# =========================================================

st.subheader("💰 2. Phương thức nhận lãi")

col1, col2, col3 = st.columns(3)

with col1:

    nhan_lai_truoc = st.checkbox(
        "☑️ Nhận lãi trước",
        key="lai_truoc_case"
    )

with col2:

    nhan_lai_hang_thang = st.checkbox(
        "☑️ Nhận lãi hàng tháng",
        key="lai_thang_case"
    )

with col3:

    nhan_lai_cuoi_ky = st.checkbox(
        "☑️ Nhận lãi cuối kỳ",
        key="lai_cuoi_ky_case"
    )


# =========================================================
# 3. NHU CẦU VỐN / VAY
# =========================================================

st.subheader("💵 3. Nhu cầu sử dụng tiền")

col1, col2 = st.columns(2)

with col1:

    co_nhu_cau_tien = st.checkbox(
        "☑️ Khách hàng cần tiền",
        key="nhu_cau_tien_case"
    )

with col2:

    co_vay_cam_co = st.checkbox(
        "☑️ Xem xét vay cầm cố sổ tiết kiệm",
        key="vay_cam_co_case"
    )


# =========================================================
# 4. CHỌN KHOẢNG THỜI GIAN TÍNH LÃI
# =========================================================

st.subheader("📅 4. Chọn khoảng thời gian tính lãi")

chon_khoang_ngay = st.checkbox(
    "☑️ Tính lãi từ ngày ... đến ngày ...",
    key="chon_khoang_ngay_case"
)


# =========================================================
# XỬ LÝ KHOẢNG NGÀY
# =========================================================

if chon_khoang_ngay:

    st.markdown("### 📅 Nhập khoảng thời gian")

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

        # -----------------------------------------------------
        # TÍNH SỐ NGÀY
        # -----------------------------------------------------

        so_ngay_khoang = (
            ngay_ket_thuc_tinh
            - ngay_bat_dau_tinh
        ).days

        # -----------------------------------------------------
        # XÁC ĐỊNH LÃI SUẤT
        # -----------------------------------------------------

        if loai_lai_khoang_ngay == "Lãi suất có kỳ hạn":

            lai_suat_ap_dung = lai_suat_co_ky_han

        else:

            lai_suat_ap_dung = lai_suat_khong_ky_han

        # -----------------------------------------------------
        # TÍNH LÃI
        # -----------------------------------------------------

        lai_khoang_ngay = tinh_lai(
            so_tien_gui,
            lai_suat_ap_dung,
            so_ngay_khoang
        )

        tong_khoang_ngay = (
            so_tien_gui
            + lai_khoang_ngay
        )

        # -----------------------------------------------------
        # HIỂN THỊ KHOẢNG NGÀY
        # -----------------------------------------------------

        st.success(
            f"""
            ✅ Đã chọn khoảng thời gian:

            **{ngay_bat_dau_tinh.strftime('%d/%m/%Y')}**
            →

            **{ngay_ket_thuc_tinh.strftime('%d/%m/%Y')}**
            """
        )

        # -----------------------------------------------------
        # KẾT QUẢ
        # -----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "⏱️ Số ngày",
                f"{so_ngay_khoang} ngày"
            )

        with col2:

            st.metric(
                "💵 Tiền lãi",
                dinh_dang_tien(
                    lai_khoang_ngay
                )
            )

        with col3:

            st.metric(
                "🏦 Gốc + lãi",
                dinh_dang_tien(
                    tong_khoang_ngay
                )
            )

        st.info(
            f"""
            **📅 Khoảng thời gian:**

            {ngay_bat_dau_tinh.strftime('%d/%m/%Y')}
            →
            {ngay_ket_thuc_tinh.strftime('%d/%m/%Y')}

            **⏱️ Số ngày:** {so_ngay_khoang} ngày

            **📈 Lãi suất áp dụng:**
            {lai_suat_ap_dung:.2f}%/năm

            **🧮 Công thức:**

            Tiền lãi =
            Tiền gốc × Lãi suất × Số ngày / 365
            """
        )


# =========================================================
# KIỂM TRA PHƯƠNG THỨC NHẬN LÃI
# =========================================================

so_phuong_thuc_lai = sum([
    nhan_lai_truoc,
    nhan_lai_hang_thang,
    nhan_lai_cuoi_ky
])

if so_phuong_thuc_lai > 1:

    st.warning(
        "⚠️ Bạn đang tích nhiều phương thức nhận lãi. "
        "Thông thường một đề chỉ chọn một phương thức."
    )


# =========================================================
# DANH SÁCH TRƯỜNG HỢP ĐÃ CHỌN
# =========================================================

cac_truong_hop = []

if rut_dung_han:

    cac_truong_hop.append(
        "Rút đúng hạn"
    )

if rut_truoc_han:

    cac_truong_hop.append(
        "Rút trước hạn"
    )

if rut_sau_han:

    cac_truong_hop.append(
        "Rút sau ngày đáo hạn"
    )

if tu_dong_gia_han:

    cac_truong_hop.append(
        "Không rút khi đến hạn / tự động gia hạn"
    )

if nhan_lai_truoc:

    cac_truong_hop.append(
        "Nhận lãi trước"
    )

if nhan_lai_hang_thang:

    cac_truong_hop.append(
        "Nhận lãi hàng tháng"
    )

if nhan_lai_cuoi_ky:

    cac_truong_hop.append(
        "Nhận lãi cuối kỳ"
    )

if co_nhu_cau_tien:

    cac_truong_hop.append(
        "Khách hàng có nhu cầu tiền"
    )

if co_vay_cam_co:

    cac_truong_hop.append(
        "Vay cầm cố sổ tiết kiệm"
    )

if chon_khoang_ngay:

    if (
        'ngay_bat_dau_tinh' in locals()
        and 'ngay_ket_thuc_tinh' in locals()
        and ngay_ket_thuc_tinh >= ngay_bat_dau_tinh
    ):

        cac_truong_hop.append(
            f"Tính lãi từ "
            f"{ngay_bat_dau_tinh.strftime('%d/%m/%Y')} "
            f"đến "
            f"{ngay_ket_thuc_tinh.strftime('%d/%m/%Y')}"
        )


st.divider()

st.subheader("📋 Các trường hợp đã chọn")

if not cac_truong_hop:

    st.warning(
        "⚠️ Chưa chọn trường hợp nào."
    )

else:

    for i, truong_hop in enumerate(
        cac_truong_hop,
        1
    ):

        st.write(
            f"**{i}. ☑️ {truong_hop}**"
        )


# =========================================================
# RÚT TRƯỚC HẠN
# =========================================================

if rut_truoc_han:

    st.divider()

    st.subheader(
        "📉 Xử lý rút trước hạn"
    )

    ngay_rut_truoc = st.date_input(
        "📅 Ngày khách hàng rút tiền",
        value=ngay_gui,
        key="ngay_rut_truoc_case"
    )

    if ngay_rut_truoc >= ngay_dao_han_ban_dau:

        st.error(
            "❌ Ngày rút phải nhỏ hơn ngày đáo hạn "
            "để được xem là rút trước hạn."
        )

    else:

        so_ngay_truoc = (
            ngay_rut_truoc
            - ngay_gui
        ).days

        lai_truoc_han = tinh_lai(
            so_tien_gui,
            lai_suat_khong_ky_han,
            so_ngay_truoc
        )

        tong_truoc_han = (
            so_tien_gui
            + lai_truoc_han
        )

        st.warning(
            "⚠️ Rút trước hạn → áp dụng lãi suất không kỳ hạn."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "⏱️ Số ngày gửi",
                f"{so_ngay_truoc} ngày"
            )

        with col2:

            st.metric(
                "💵 Tiền lãi",
                dinh_dang_tien(
                    lai_truoc_han
                )
            )

        with col3:

            st.metric(
                "🏦 Tổng tiền nhận",
                dinh_dang_tien(
                    tong_truoc_han
                )
            )

        st.info(
            f"""
            **Lãi suất áp dụng:**
            {lai_suat_khong_ky_han:.2f}%/năm

            **Công thức:**

            Tiền lãi =
            Tiền gốc × Lãi suất × Số ngày / 365
            """
        )


# =========================================================
# RÚT ĐÚNG HẠN
# =========================================================

if rut_dung_han:

    st.divider()

    st.subheader(
        "📈 Xử lý rút đúng hạn"
    )

    so_ngay_dung_han = (
        ngay_dao_han_ban_dau
        - ngay_gui
    ).days

    lai_dung_han = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        so_ngay_dung_han
    )

    tong_dung_han = (
        so_tien_gui
        + lai_dung_han
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "⏱️ Số ngày gửi",
            f"{so_ngay_dung_han} ngày"
        )

    with col2:

        st.metric(
            "💵 Tiền lãi",
            dinh_dang_tien(
                lai_dung_han
            )
        )

    with col3:

        st.metric(
            "🏦 Tổng tiền nhận",
            dinh_dang_tien(
                tong_dung_han
            )
        )

    st.success(
        f"""
        ✅ Rút đúng ngày đáo hạn.

        **Lãi suất:**
        {lai_suat_co_ky_han:.2f}%/năm
        """
    )


# =========================================================
# RÚT SAU NGÀY ĐÁO HẠN
# =========================================================

if rut_sau_han:

    st.divider()

    st.subheader(
        "🔄 Xử lý rút sau ngày đáo hạn"
    )

    ngay_rut_sau = st.date_input(
        "📅 Ngày khách hàng rút tiền",
        value=ngay_dao_han_ban_dau,
        key="ngay_rut_sau_case"
    )

    if ngay_rut_sau <= ngay_dao_han_ban_dau:

        st.error(
            "❌ Ngày rút phải lớn hơn ngày đáo hạn."
        )

    else:

        so_ngay_sau_han = (
            ngay_rut_sau
            - ngay_dao_han_ban_dau
        ).days

        lai_ky_han = tinh_lai(
            so_tien_gui,
            lai_suat_co_ky_han,
            (
                ngay_dao_han_ban_dau
                - ngay_gui
            ).days
        )

        tien_sau_dao_han = (
            so_tien_gui
            + lai_ky_han
        )

        lai_sau_han = tinh_lai(
            tien_sau_dao_han,
            lai_suat_khong_ky_han,
            so_ngay_sau_han
        )

        tong_sau_han = (
            tien_sau_dao_han
            + lai_sau_han
        )

        st.warning(
            """
            ⚠️ Khoản tiền đã qua ngày đáo hạn.

            Phần thời gian sau đáo hạn đang được tính
            theo lãi suất không kỳ hạn.
            """
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "⏱️ Số ngày sau đáo hạn",
                f"{so_ngay_sau_han} ngày"
            )

        with col2:

            st.metric(
                "💵 Lãi sau đáo hạn",
                dinh_dang_tien(
                    lai_sau_han
                )
            )

        with col3:

            st.metric(
                "🏦 Tổng tiền nhận",
                dinh_dang_tien(
                    tong_sau_han
                )
            )


# =========================================================
# NHẬN LÃI TRƯỚC
# =========================================================

if nhan_lai_truoc:

    st.divider()

    st.subheader(
        "💳 Xử lý nhận lãi trước"
    )

    so_ngay_ky = (
        ngay_dao_han_ban_dau
        - ngay_gui
    ).days

    lai_nhan_truoc = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        so_ngay_ky
    )

    st.metric(
        "💵 Tiền lãi nhận trước",
        dinh_dang_tien(
            lai_nhan_truoc
        )
    )

    st.info(
        """
        Tiền lãi được trả trước cho khách hàng.

        Tiền gốc tiếp tục duy trì trong sổ.
        """
    )


# =========================================================
# NHẬN LÃI HÀNG THÁNG
# =========================================================

if nhan_lai_hang_thang:

    st.divider()

    st.subheader(
        "💳 Xử lý nhận lãi hàng tháng"
    )

    so_ngay_ky = (
        ngay_dao_han_ban_dau
        - ngay_gui
    ).days

    lai_toan_ky = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        so_ngay_ky
    )

    lai_moi_thang = (
        lai_toan_ky / ky_han
        if ky_han > 0
        else 0
    )

    st.metric(
        "💵 Tiền lãi dự kiến mỗi tháng",
        dinh_dang_tien(
            lai_moi_thang
        )
    )

    st.info(
        """
        Tiền lãi được trả định kỳ hàng tháng.

        Tiền gốc tiếp tục được duy trì.
        """
    )


# =========================================================
# NHẬN LÃI CUỐI KỲ
# =========================================================

if nhan_lai_cuoi_ky:

    st.divider()

    st.subheader(
        "💳 Xử lý nhận lãi cuối kỳ"
    )

    so_ngay_ky = (
        ngay_dao_han_ban_dau
        - ngay_gui
    ).days

    lai_cuoi_ky = tinh_lai(
        so_tien_gui,
        lai_suat_co_ky_han,
        so_ngay_ky
    )

    tong_cuoi_ky = (
        so_tien_gui
        + lai_cuoi_ky
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💵 Tiền lãi",
            dinh_dang_tien(
                lai_cuoi_ky
            )
        )

    with col2:

        st.metric(
            "🏦 Gốc + lãi",
            dinh_dang_tien(
                tong_cuoi_ky
            )
        )


# =========================================================
# TỰ ĐỘNG GIA HẠN
# =========================================================

if tu_dong_gia_han:

    st.divider()

    st.subheader(
        "🔄 Xử lý tự động gia hạn"
    )

    so_ky_mo_phong = st.number_input(
        "🔢 Số kỳ muốn mô phỏng",
        min_value=1,
        max_value=50,
        value=2,
        step=1,
        key="so_ky_mo_phong_case"
    )

    tien_goc_hien_tai = so_tien_gui

    ngay_bd_ky = ngay_gui

    tong_lai_gia_han = 0

    bang_gia_han = []

    for ky in range(
        1,
        int(so_ky_mo_phong) + 1
    ):

        ngay_kt_ky = tinh_ngay_dao_han(
            ngay_bd_ky,
            ky_han
        )

        so_ngay_ky = (
            ngay_kt_ky
            - ngay_bd_ky
        ).days

        lai_ky = tinh_lai(
            tien_goc_hien_tai,
            lai_suat_co_ky_han,
            so_ngay_ky
        )

        goc_dau_ky = tien_goc_hien_tai

        if nhan_lai_cuoi_ky:

            tien_goc_hien_tai += lai_ky

        tong_lai_gia_han += lai_ky

        bang_gia_han.append(
            {
                "Kỳ": ky,
                "Ngày bắt đầu":
                    ngay_bd_ky.strftime(
                        "%d/%m/%Y"
                    ),
                "Ngày đáo hạn":
                    ngay_kt_ky.strftime(
                        "%d/%m/%Y"
                    ),
                "Số ngày":
                    so_ngay_ky,
                "Tiền gốc đầu kỳ":
                    round(goc_dau_ky),
                "Tiền lãi":
                    round(lai_ky),
                "Tiền gốc sau gia hạn":
                    round(tien_goc_hien_tai)
            }
        )

        ngay_bd_ky = ngay_kt_ky

    df_gia_han = pd.DataFrame(
        bang_gia_han
    )

    st.dataframe(
        df_gia_han,
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💵 Tổng lãi các kỳ",
            dinh_dang_tien(
                tong_lai_gia_han
            )
        )

    with col2:

        st.metric(
            "🏦 Gốc sau mô phỏng",
            dinh_dang_tien(
                tien_goc_hien_tai
            )
        )


# =========================================================
# KHÁCH HÀNG CẦN TIỀN
# =========================================================

if co_nhu_cau_tien:

    st.divider()

    st.subheader(
        "💰 Xử lý nhu cầu cần tiền"
    )

    ngay_can_tien = st.date_input(
        "📅 Ngày khách hàng cần tiền",
        value=ngay_dao_han_ban_dau,
        key="ngay_can_tien_case"
    )

    so_tien_can = st.number_input(
        "💵 Số tiền khách hàng cần (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        key="so_tien_can_case"
    )

    if ngay_can_tien < ngay_dao_han_ban_dau:

        st.warning(
            """
            ⚠️ Khách hàng cần tiền trước ngày đáo hạn.

            Có thể so sánh:

            1. Rút trước hạn.
            2. Vay cầm cố sổ tiết kiệm.
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

    st.subheader(
        "🏦 Xử lý vay cầm cố sổ tiết kiệm"
    )

    so_tien_vay = st.number_input(
        "💰 Số tiền vay (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        key="so_tien_vay_case"
    )

    lai_suat_vay = st.number_input(
        "📈 Lãi suất vay (%/năm)",
        min_value=0.0,
        value=8.0,
        step=0.1,
        format="%.2f",
        key="lai_suat_vay_case"
    )

    so_ngay_vay = st.number_input(
        "📅 Số ngày vay",
        min_value=1,
        value=3,
        step=1,
        key="so_ngay_vay_case"
    )

    lai_vay = (
        so_tien_vay
        * lai_suat_vay / 100
        * so_ngay_vay
        / 365
    )

    tong_tra_vay = (
        so_tien_vay
        + lai_vay
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💵 Tiền lãi vay",
            dinh_dang_tien(
                lai_vay
            )
        )

    with col2:

        st.metric(
            "🏦 Tổng tiền phải trả",
            dinh_dang_tien(
                tong_tra_vay
            )
        )

    st.info(
        """
        **Công thức:**

        Tiền lãi vay =
        Tiền vay × Lãi suất vay × Số ngày vay / 365
        """
    )


# =========================================================
# BẢNG TÓM TẮT
# =========================================================

if cac_truong_hop:

    st.divider()

    st.subheader(
        "📑 Tóm tắt trường hợp đã chọn"
    )

    df_tom_tat = pd.DataFrame(
        {
            "STT":
                range(
                    1,
                    len(cac_truong_hop) + 1
                ),
            "Trường hợp":
                cac_truong_hop
        }
    )

    st.dataframe(
        df_tom_tat,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CHÂN TRANG
# =========================================================

st.divider()

st.caption(
    "🏦 Ứng dụng tính lãi tiền gửi tiết kiệm - Streamlit"
)

st.caption(
    "📚 Công cụ xử lý các trường hợp trong bài tập"
)
