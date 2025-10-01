import streamlit as st
from schedule_generator import generate_weekly_schedule

# --------------------------
# Fixed Subject List
# --------------------------
subject_options = {
    1: "Bahasa Melayu",
    2: "English",
    3: "Chinese",
    4: "Science",
    5: "Mathematics",
    6: "Sejarah",
    7: "Geografi",
    8: "Account",
    9: "Pendidikan Seni Visual",
    10: "Sains Komputer",
    11: "Pendidikan Moral",
    12: "Pendidikan Islam",
    13: "Additional Mathematics",
    14: "Physics",
    15: "Biologi",
    16: "Chemistry",
}

# --------------------------
# Categories (for user clarity only)
# --------------------------
categories = ["Tingkatan 1-3", "Sastera", "Sains"]

# --------------------------
# Streamlit Page Config
# --------------------------
st.set_page_config(page_title="📚 Penjana Jadual Ulang Kaji", layout="centered")

# --------------------------
# Custom CSS - Motion Gradient Background
# --------------------------
page_bg = """
<style>
/* Full-screen animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #3a6186);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Beautify buttons */
div.stButton > button {
    background-color: #1e3c72;
    color: white;
    border-radius: 10px;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: bold;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #2a5298;
    transform: scale(1.05);
}

/* White text for all inputs */
.css-1cpxqw2, .css-1d391kg, label, .stText, .stNumberInput input {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --------------------------
# Title
# --------------------------
st.markdown("<h1 style='text-align: center;'>📚 Penjana Jadual Ulang Kaji</h1>", unsafe_allow_html=True)

# --------------------------
# Step 1: Category Selection
# --------------------------
selected_category = st.selectbox("Pilih Kategori Murid", categories)

# --------------------------
# Step 2: Subject Selection (FINAL FIX)
# --------------------------
st.subheader("🎯 Pilih Subjek")

# ensure session state key exists
if "selected_subjects" not in st.session_state:
    st.session_state.selected_subjects = []

subjects_list = list(subject_options.values())

# callbacks for buttons
def _select_all():
    st.session_state.selected_subjects = subjects_list.copy()

def _clear_all():
    st.session_state.selected_subjects = []

col_main, col_buttons = st.columns([4, 1])

with col_main:
    st.multiselect(
        "Pilih Subjek (boleh pilih lebih daripada satu)",
        options=subjects_list,
        key="selected_subjects",
        help="Klik untuk buka menu, pilih beberapa subjek sekaligus, kemudian klik di luar untuk tutup."
    )

with col_buttons:
    st.write("")  # spacing
    st.button("✅ Pilih Semua", on_click=_select_all)
    st.write("❌ Kosongkan Semua", on_click=_clear_all)

# now you can use this safely
selected_subjects = st.session_state.selected_subjects


# --------------------------
# Step 3: Difficulty Sliders (Auto appear after subject selection)
# --------------------------
st.subheader("⚡ Tahap Kesukaran Subjek (1 = mudah, 5 = susah)")
difficulties = {}
if selected_subjects:
    for subj in selected_subjects:
        difficulties[subj] = st.slider(f"{subj}", min_value=1, max_value=5, value=3)

# --------------------------
# Step 4: Study Settings
# --------------------------
st.subheader("⏰ Tetapan Masa Belajar")
daily_hours = st.number_input("Jam Belajar Sehari", min_value=1, max_value=12, value=4)
subjects_per_day = st.number_input("Bilangan Subjek Sehari", min_value=1, max_value=10, value=3)

# --------------------------
# Step 5: Generate Schedule
# --------------------------
if st.button("🚀 Jana Jadual"):
    if not selected_subjects:
        st.error("Sila pilih sekurang-kurangnya satu subjek!")
    else:
        schedule = generate_weekly_schedule(
            selected_subjects,
            difficulties,
            daily_hours,
            subjects_per_day
        )

        st.success(f"✅ Jadual Ulang Kaji untuk kategori {selected_category} telah dijana!")
        for day, info in schedule.items():
            st.markdown(f"### {day}")
            for subj, v in info.items():
                st.write(f"- **{subj}**: {v['minutes']} min ({v['hours']} jam)")
