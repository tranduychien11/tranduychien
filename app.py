import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản lý điểm sinh viên", layout="centered")

data = {
    "Ho_ten":     ["An", "Bình", "Chi", "Dũng", "Hà", "Lan", "Minh", "Nam", "Phúc", "Trang"],
    "Chuyen_can": [9, 8, 7, 10, 8, 6, 9, 7, 8, 10],
    "Giua_ky":    [7.5, 8, 6, 8.5, 6.5, 4.5, 8, 6.5, 7, 9],
    "Cuoi_ky":    [7.5, 8, 6, 9, 6.5, 4, 8.5, 6.5, 6.5, 9],
}
df = pd.DataFrame(data)
df["Tong_ket"] = (0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]).round(2)


def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

st.subheader("Bảng điểm")
bang = df.rename(columns={
    "Ho_ten": "Họ tên", "Chuyen_can": "Chuyên cần", "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ", "Tong_ket": "Tổng kết", "Xep_loai": "Xếp loại",
})
st.dataframe(bang, use_container_width=True, hide_index=True)

st.subheader("Thống kê")
cao = df.loc[df["Tong_ket"].idxmax()]
thap = df.loc[df["Tong_ket"].idxmin()]
so_dat = int((df["Tong_ket"] >= 5).sum())

c1, c2 = st.columns(2)
c1.metric("Điểm trung bình lớp", f"{df['Tong_ket'].mean():.2f}")
c2.metric("Số sinh viên đạt", f"{so_dat}/{len(df)}")
st.write(f"**Cao nhất:** {cao['Ho_ten']} ({cao['Tong_ket']})")
st.write(f"**Thấp nhất:** {thap['Ho_ten']} ({thap['Tong_ket']})")

st.subheader("Tra cứu sinh viên")
ten = st.selectbox("Chọn sinh viên", df["Ho_ten"])
sv = df[df["Ho_ten"] == ten].iloc[0]
st.write(f"- Chuyên cần: **{sv['Chuyen_can']}**")
st.write(f"- Giữa kỳ: **{sv['Giua_ky']}**")
st.write(f"- Cuối kỳ: **{sv['Cuoi_ky']}**")
st.write(f"- Điểm tổng kết: **{sv['Tong_ket']}**")
st.write(f"- Xếp loại: **{sv['Xep_loai']}**")

st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(df["Ho_ten"], df["Tong_ket"], color="#4C8BF5")
ax.invert_yaxis()
ax.set_xlim(0, 10)
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Sinh viên")
ax.set_title("Điểm tổng kết của 10 sinh viên")
st.pyplot(fig)

st.markdown("---")
st.markdown(
    "<p style='font-size:12px; color:gray;'>Người thực hiện: "
    "<b>Tran Duy Chien</b> - MSSV: <b>052208004600</b></p>",
    unsafe_allow_html=True,
)
