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
# BÀI TẬP TRÊN LỚP - 4 YÊU CẦU
# =========================================================

st.divider()

st.header("📝 GIẢI BÀI TẬP THEO ĐỀ")


# =========================================================
# DỮ LIỆU ĐỀ BÀI
# =========================================================

tien_de = 500_000_000

ngay_gui_de = date(2026, 8, 23)

ngay_dao_han_de = date(2026, 11, 23)

lai_suat_co_han_de = 5.0

lai_suat_khong_han_de = 0.2

lai_suat_vay_de = 8.0

ngay_rut_cau_2 = date(2026, 9, 26)

ngay_rut_cau_3 = date(2026, 10, 10)

ngay_can_tien = date(2026, 11, 26)


# =========================================================
# HIỂN THỊ DỮ LIỆU ĐỀ
# =========================================================

with st.expander(
    "📌 Xem dữ liệu đề bài",
    expanded=True
):

    st.write(
        f"""
        💰 **Số tiền gửi:** {dinh_dang_tien(tien_de)}

        📅 **Ngày gửi:** {ngay_gui_de.strftime('%d/%m/%Y')}

        ⏳ **Kỳ hạn:** 3 tháng

        📅 **Ngày đáo hạn:** {ngay_dao_han_de.strftime('%d/%m/%Y')}

        📈 **Lãi suất có kỳ hạn:** {lai_suat_co_han_de}%/năm

        📉 **Lãi suất không kỳ hạn:** {lai_suat_khong_han_de}%/năm

        💳 **Phương thức:** Nhận lãi cuối kỳ

        🏦 **Lãi suất vay cầm cố:** {lai_suat_vay_de}%/năm
        """
    )


# =========================================================
# CÂU 1
# =========================================================

st.subheader(
    "🔹 Câu 1. Số tiền khách hàng nhận được vào thời điểm đáo hạn"
)

so_ngay_c1, lai_c1 = tinh_lai_bai(
    tien_de,
    lai_suat_co_han_de,
    ngay_gui_de,
    ngay_dao_han_de
)

tong_c1 = tien_de + lai_c1


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⏱️ Số ngày gửi",
        f"{so_ngay_c1} ngày"
    )

with col2:

    st.metric(
        "💵 Tiền lãi",
        dinh_dang_tien(lai_c1)
    )

with col3:

    st.metric(
        "🏦 Tổng tiền nhận",
        dinh_dang_tien(tong_c1)
    )


st.info(
    f"""
    ### Công thức câu 1

    Tiền lãi:

    **500.000.000 × 5% × {so_ngay_c1} / 365**

    = **{dinh_dang_tien(lai_c1)}**

    Tổng tiền nhận:

    **500.000.000 + {dinh_dang_tien(lai_c1)}**

    = **{dinh_dang_tien(tong_c1)}**
    """
)


# =========================================================
# CÂU 2
# =========================================================

st.subheader(
    "🔹 Câu 2. Nếu ngày 26/09/2026 khách hàng rút tiền"
)

so_ngay_c2, lai_c2 = tinh_lai_bai(
    tien_de,
    lai_suat_khong_han_de,
    ngay_gui_de,
    ngay_rut_cau_2
)

tong_c2 = tien_de + lai_c2


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⏱️ Số ngày gửi",
        f"{so_ngay_c2} ngày"
    )

with col2:

    st.metric(
        "💵 Tiền lãi",
        dinh_dang_tien(lai_c2)
    )

with col3:

    st.metric(
        "🏦 Tổng tiền nhận",
        dinh_dang_tien(tong_c2)
    )


st.warning(
    f"""
    ⚠️ Khách hàng rút trước hạn.

    Lãi suất áp dụng:
    **{lai_suat_khong_han_de}%/năm**

    Tiền lãi:

    **500.000.000 × 0,2% × {so_ngay_c2} / 365**

    = **{dinh_dang_tien(lai_c2)}**

    Tổng tiền nhận:

    = **{dinh_dang_tien(tong_c2)}**
    """
)


# =========================================================
# CÂU 3
# =========================================================

st.subheader(
    "🔹 Câu 3. Nếu ngày 10/10/2026 khách hàng rút tiền"
)

so_ngay_c3, lai_c3 = tinh_lai_bai(
    tien_de,
    lai_suat_khong_han_de,
    ngay_gui_de,
    ngay_rut_cau_3
)

tong_c3 = tien_de + lai_c3


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⏱️ Số ngày gửi",
        f"{so_ngay_c3} ngày"
    )

with col2:

    st.metric(
        "💵 Tiền lãi",
        dinh_dang_tien(lai_c3)
    )

with col3:

    st.metric(
        "🏦 Tổng tiền nhận",
        dinh_dang_tien(tong_c3)
    )


st.warning(
    f"""
    ⚠️ Khách hàng rút trước hạn.

    Lãi suất áp dụng:
    **{lai_suat_khong_han_de}%/năm**

    Tiền lãi:

    **500.000.000 × 0,2% × {so_ngay_c3} / 365**

    = **{dinh_dang_tien(lai_c3)}**

    Tổng tiền nhận:

    = **{dinh_dang_tien(tong_c3)}**
    """
)


# =========================================================
# CÂU 4
# =========================================================

st.subheader(
    "🔹 Câu 4. Khách hàng cần 500.000.000 VNĐ ngày 26/11/2026"
)


so_tien_can = 500_000_000


st.write(
    f"""
    📅 Ngày cần tiền:
    **{ngay_can_tien.strftime('%d/%m/%Y')}**

    💰 Số tiền cần:
    **{dinh_dang_tien(so_tien_can)}**

    📅 Ngày đáo hạn:
    **{ngay_dao_han_de.strftime('%d/%m/%Y')}**
    """
)


# =========================================================
# PHƯƠNG ÁN 1
# GIỮ TIỀN ĐẾN ĐÁO HẠN
# =========================================================

tien_nhan_dao_han = tong_c1

tien_du = (
    tien_nhan_dao_han
    - so_tien_can
)


# =========================================================
# PHƯƠNG ÁN 2
# VAY CẦM CỐ SỔ TIẾT KIỆM
# =========================================================

# Nếu vay 500 triệu trong 3 ngày:
so_ngay_vay = (
    ngay_can_tien
    - ngay_dao_han_de
).days

lai_vay = (
    so_tien_can
    * lai_suat_vay_de / 100
    * so_ngay_vay
    / 365
)

tong_tra_vay = (
    so_tien_can
    + lai_vay
)


# =========================================================
# HIỂN THỊ SO SÁNH
# =========================================================

st.markdown("### 📊 So sánh 2 phương án")


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "#### 🟢 Phương án 1: Giữ đến đáo hạn"
    )

    st.metric(
        "Tiền nhận ngày 23/11",
        dinh_dang_tien(
            tien_nhan_dao_han
        )
    )

    st.metric(
        "Sau khi lấy 500 triệu",
        dinh_dang_tien(
            tien_du
        )
    )


with col2:

    st.markdown(
        "#### 🔴 Phương án 2: Vay cầm cố"
    )

    st.metric(
        "Lãi suất vay",
        f"{lai_suat_vay_de}%/năm"
    )

    st.metric(
        "Số ngày vay",
        f"{so_ngay_vay} ngày"
    )

    st.metric(
        "Tiền lãi vay",
        dinh_dang_tien(
            lai_vay
        )
    )


# =========================================================
# KẾT LUẬN CÂU 4
# =========================================================

if tien_nhan_dao_han >= so_tien_can:

    st.success(
        f"""
        ## ✅ TƯ VẤN KHÁCH HÀNG

        **Khách hàng nên giữ khoản tiền gửi đến ngày
        đáo hạn 23/11/2026.**

        Khi đáo hạn, khách hàng nhận:

        ### 🏦 {dinh_dang_tien(tien_nhan_dao_han)}

        Sau đó khách hàng cần 500 triệu vào ngày 26/11/2026.

        Số tiền còn lại:

        ### 💰 {dinh_dang_tien(tien_du)}

        **Không cần vay cầm cố sổ tiết kiệm**, vì khoản tiền gửi
        đã đáo hạn trước ngày khách hàng cần tiền.

        Nếu vay 500 triệu với lãi suất 8%/năm trong 3 ngày,
        riêng tiền lãi vay khoảng:

        ### 💸 {dinh_dang_tien(lai_vay)}

        👉 Vì vậy, phương án hợp lý nhất là:

        **Giữ tiền đến ngày đáo hạn → nhận cả gốc và lãi
        → sử dụng 500 triệu vào ngày 26/11/2026.**
        """
    )

else:

    st.error(
        """
        ❌ Khoản tiền nhận khi đáo hạn không đủ 500 triệu.
        Khách hàng cần xem xét phương án vay.
        """
    )


# =========================================================
# BẢNG TỔNG HỢP 3 TRƯỜNG HỢP
# =========================================================

st.divider()

st.subheader(
    "📑 Bảng tổng hợp kết quả"
)


bang_ket_qua = pd.DataFrame(
    {
        "Trường hợp": [
            "Rút đúng hạn 23/11/2026",
            "Rút trước hạn 26/09/2026",
            "Rút trước hạn 10/10/2026"
        ],

        "Số ngày gửi": [
            so_ngay_c1,
            so_ngay_c2,
            so_ngay_c3
        ],

        "Lãi suất (%/năm)": [
            lai_suat_co_han_de,
            lai_suat_khong_han_de,
            lai_suat_khong_han_de
        ],

        "Tiền lãi (VNĐ)": [
            round(lai_c1),
            round(lai_c2),
            round(lai_c3)
        ],

        "Tổng tiền nhận (VNĐ)": [
            round(tong_c1),
            round(tong_c2),
            round(tong_c3)
        ]
    }
)


st.dataframe(
    bang_ket_qua,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TÓM TẮT ĐÁP ÁN
# =========================================================

st.subheader(
    "🎯 Tóm tắt đáp án bài tập"
)

st.write(
    f"""
    **Câu 1:** Khách hàng nhận
    **{dinh_dang_tien(tong_c1)}**
    khi đáo hạn.

    **Câu 2:** Nếu rút ngày 26/09/2026,
    khách hàng nhận **{dinh_dang_tien(tong_c2)}**.

    **Câu 3:** Nếu rút ngày 10/10/2026,
    khách hàng nhận **{dinh_dang_tien(tong_c3)}**.

    **Câu 4:** Nên **giữ tiền đến ngày đáo hạn 23/11/2026**,
    nhận gốc + lãi rồi sử dụng 500 triệu vào ngày 26/11/2026.
    Không cần vay cầm cố sổ tiết kiệm.
    """
)


# =========================================================
# CHÂN TRANG
# =========================================================

st.divider()

st.caption(
    "🏦 Ứng dụng tính lãi tiền gửi tiết kiệm - Streamlit"
)

st.caption(
    "📚 Bài tập tính lãi tiền gửi ngân hàng"
)
