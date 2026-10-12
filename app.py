# QUAN LY DIEM SINH VIEN - STREAMLIT

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CAU HINH TRANG WEB
st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="📚",
    layout="wide"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. TAO DU LIEU
data = {
    "Ho_ten": [
        "Nguyen Van An",
        "Tran Thi Binh",
        "Le Van Cuong",
        "Pham Thi Dung",
        "Hoang Van Em",
        "Vu Thi Giang",
        "Do Van Hung",
        "Bui Thi Lan",
        "Dang Van Minh",
        "Nguyen Thi Hoa"
    ],
    "Chuyen_can": [9, 8, 7, 10, 6, 9, 5, 8, 7, 10],
    "Giua_ky": [8, 7, 6, 9, 5, 8, 4, 7, 6, 9],
    "Cuoi_ky": [9, 8, 7, 9, 4, 9, 5, 8, 7, 10]
}

df = pd.DataFrame(data)

# 3. TINH DIEM TONG KET
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
)

# 4. XEP LOAI
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 5. HIEN THI BANG DIEM
st.header("1. Bảng điểm sinh viên")

bang_diem = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_diem.style.format({"Tổng kết": "{:.2f}"}),
    use_container_width=True,
    hide_index=True
)

# 6. THONG KE
st.header("2. Thống kê kết quả")

diem_tb = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = int((df["Tong_ket"] >= 5).sum())

cot1, cot2, cot3 = st.columns(3)

cot1.metric("Điểm trung bình", f"{diem_tb:.2f}")
cot2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")
cot3.metric("Điểm cao nhất", f"{sv_max['Tong_ket']:.2f}")

st.write(
    f"**Sinh viên cao nhất:** {sv_max['Ho_ten']} "
    f"({sv_max['Tong_ket']:.2f} điểm)"
)

st.write(
    f"**Sinh viên thấp nhất:** {sv_min['Ho_ten']} "
    f"({sv_min['Tong_ket']:.2f} điểm)"
)

# 7. CHON SINH VIEN
st.header("3. Tra cứu sinh viên")

ten_sv = st.selectbox(
    "Chọn một sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.subheader(f"Thông tin sinh viên: {ten_sv}")

c1, c2, c3 = st.columns(3)
c1.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
c2.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
c3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")

c4, c5 = st.columns(2)
c4.metric("Điểm tổng kết", f"{sv['Tong_ket']:.2f}")
c5.metric("Xếp loại", sv["Xep_loai"])

# 8. BIEU DO
st.header("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)

plt.xticks(rotation=45, ha="right")
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 9. THONG TIN NGUOI TAO
st.divider()

st.caption("Người tạo ứng dụng: [Họ tên của bạn] | MSSV: [Mã số sinh viên]")
