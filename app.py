# ==========================
# Nhập dữ liệu
# ==========================

tien_gui = st.number_input(
    "💰 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500000000.0,
    step=1000000.0,
    format="%.0f"
)

# Chọn loại tiền gửi
loai_gui = st.selectbox(
    "🏦 Loại tiền gửi",
    ["Có kỳ hạn", "Không kỳ hạn"]
)

# Nhập lãi suất
if loai_gui == "Có kỳ hạn":
    lai_suat = st.number_input(
        "📈 Lãi suất kỳ hạn (%)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )
else:
    lai_suat = st.number_input(
        "📈 Lãi suất không kỳ hạn (%)",
        min_value=0.0,
        value=0.2,
        step=0.01
    )

don_vi_lai = st.selectbox(
    "📌 Đơn vị lãi suất",
    [
        "Theo năm",
        "Theo tháng",
        "Theo ngày"
    ]
)

ngay_gui = st.date_input(
    "📅 Ngày gửi",
    value=date.today()
)

ngay_dao_han = st.date_input(
    "📅 Ngày đáo hạn",
    value=date.today()
)

st.info(f"🏦 Hình thức gửi: **{loai_gui}**")
