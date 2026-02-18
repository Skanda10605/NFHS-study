import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from venn import venn

# set up page configuration and layout
st.set_page_config(page_title="Health Marker Visualizer", layout="wide")

# apply custom dark theme styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #121212;
        color: #f5f5f5;
    }

    .stApp {
        background-color: #121212;
    }

    h1, h2, h3, h4 {
        color: #f5f5f5;
    }

    p, label, span {
        color: #dddddd !important;
        font-size: 1rem;
    }

    .stTextInput > div > div > input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444;
        border-radius: 6px;
        padding: 0.5rem;
    }

    .stButton>button {
        background-color: #2e86de;
        color: white;
        font-weight: 600;
        font-size: 16px;
        border-radius: 6px;
        padding: 0.5em 1.2em;
        border: none;
        margin-top: 1rem;
    }

    .stButton>button:hover {
        background-color: #1b4f72;
    }

    .block {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }

    .css-18ni7ap, .css-1aumxhk {
        color: #f5f5f5 !important;
    }

    </style>
""", unsafe_allow_html=True)

# display page title and description
st.markdown("<h1 style='text-align: center;'>Health Marker Visualizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Upload your data to explore overlaps and correlations between health indicators.</p>", unsafe_allow_html=True)

# handle file upload and input fields
with st.container():
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("Upload & Parameters")

    uploaded_file = st.file_uploader("Upload your `.csv` file", type=["csv"])

    # organize input fields into two columns
    col1, col2 = st.columns(2)
    with col1:
        haem_lb = st.text_input("Hemoglobin Lower Bound (g/dl)", value="")
        bmi_lb = st.text_input("BMI Lower Bound", value="")
        press_lb = st.text_input("Systolic Pressure Lower Bound", value="")
        glu_ub = st.text_input("Glucose Upper Bound (mg/dL)", value="")

    with col2:
        haem_ub = st.text_input("Hemoglobin Upper Bound (g/dl)", value="")
        bmi_ub = st.text_input("BMI Upper Bound", value="")
        press_ub = st.text_input("Systolic Pressure Upper Bound", value="")

    generate = st.button("Generate Visualizations")
    st.markdown("</div>", unsafe_allow_html=True)

# generate outputs if everything is filled
if generate:
    if not uploaded_file:
        st.error("please upload a CSV file.")
    elif not all([haem_lb, haem_ub, bmi_lb, bmi_ub, press_lb, press_ub, glu_ub]):
        st.error("please fill in all the input fields.")
    else:
        try:
            # convert all input values to floats
            haem_lb = float(haem_lb)
            haem_ub = float(haem_ub)
            bmi_lb = float(bmi_lb)
            bmi_ub = float(bmi_ub)
            press_lb = float(press_lb)
            press_ub = float(press_ub)
            glu_ub = float(glu_ub)

            # load data from uploaded csv
            pdf = pd.read_csv(uploaded_file)

            # calculate mean of 3 systolic readings
            pdf['Mean systolic reading'] = (pdf['sb18s'] + pdf['sb25s'] + pdf['sb29s']) / 3

            # create binary features for health indicators
            df = pd.DataFrame()
            df['Normal bmi'] = ((pdf['v445'] >= bmi_lb) & (pdf['v445'] <= bmi_ub)).astype(int)
            df['Normal systolic pressure'] = ((pdf['Mean systolic reading'] >= press_lb) & (pdf['Mean systolic reading'] <= press_ub)).astype(int)
            df['Normal haemoglobin'] = ((pdf['v453'] >= haem_lb) & (pdf['v453'] <= haem_ub)).astype(int)
            df['normal glucose'] = (pdf['sb74'] <= glu_ub).astype(int)

            # plot venn diagram
            st.markdown("<div class='block'>", unsafe_allow_html=True)
            st.subheader("Venn Diagram")
            data_dict = {feat: set(df.index[df[feat] == 1]) for feat in df.columns}
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            venn(data_dict, ax=ax1)
            ax1.set_title("Overlap of Normal Health Indicators", fontsize=14)
            st.pyplot(fig1)
            st.markdown("</div>", unsafe_allow_html=True)

            # plot correlation heatmap
            st.markdown("<div class='block'>", unsafe_allow_html=True)
            st.subheader("Correlation Heatmap")
            corr = df.corr()
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            sns.heatmap(
                corr,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                vmin=0,
                vmax=1,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8}
            )
            ax2.set_title("Correlation between Binary Features", fontsize=14)
            st.pyplot(fig2)
            st.markdown("</div>", unsafe_allow_html=True)

            st.success("visualization complete!")

        except Exception as e:
            st.error(f"error: {e}")
