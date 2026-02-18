import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def process_raw_data(pdf, bmi_lb, bmi_ub, press_lb, press_ub, haem_lb, haem_ub, glu_ub):
    """Process raw health data and create normal/abnormal indicators"""
    
    # Calculate mean of 3 systolic readings
    if all(col in pdf.columns for col in ['sb18s', 'sb25s', 'sb29s']):
        pdf['Mean systolic reading'] = (pdf['sb18s'] + pdf['sb25s'] + pdf['sb29s']) / 3
    else:
        st.warning("Systolic pressure columns (sb18s, sb25s, sb29s) not found. Using alternative approach.")
        systolic_cols = [col for col in pdf.columns if 'systolic' in col.lower() or 'sb' in col.lower()]
        if systolic_cols:
            st.info(f"Using column: {systolic_cols[0]} for systolic pressure")
            pdf['Mean systolic reading'] = pdf[systolic_cols[0]]
        else:
            st.error("No systolic pressure data found")
            return None
    
    # Required columns
    required_mapping = {
        'v445': 'BMI',
        'v453': 'Haemoglobin', 
        'sb74': 'Glucose'
    }
    
    missing_cols = [f"{col} ({name})" for col, name in required_mapping.items() if col not in pdf.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
        st.info("Available columns:")
        st.write(list(pdf.columns))
        return None
    
    df = pd.DataFrame()
    df['Normal bmi'] = ((pdf['v445'] >= bmi_lb) & (pdf['v445'] <= bmi_ub)).astype(int)
    df['Normal systolic pressure'] = ((pdf['Mean systolic reading'] >= press_lb) & (pdf['Mean systolic reading'] <= press_ub)).astype(int)
    df['Normal haemoglobin'] = ((pdf['v453'] >= haem_lb) & (pdf['v453'] <= haem_ub)).astype(int)
    df['Normal glucose'] = (pdf['sb74'] <= glu_ub).astype(int)
    
    # Raw values
    df['BMI_value'] = pdf['v445']
    df['Systolic_value'] = pdf['Mean systolic reading']
    df['Haemoglobin_value'] = pdf['v453']
    df['Glucose_value'] = pdf['sb74']
    
    return df

def analyze_health_data(df):
    """Analyze processed health data and return visualizations"""
    df['Abnormal bmi'] = 1 - df['Normal bmi']
    df['Abnormal systolic pressure'] = 1 - df['Normal systolic pressure']
    df['Abnormal glucose'] = 1 - df['Normal glucose']
    df['Abnormal haemoglobin'] = 1 - df['Normal haemoglobin']
    
    abnormality_cols = [
        'Abnormal bmi',
        'Abnormal systolic pressure',
        'Abnormal glucose',
        'Abnormal haemoglobin'
    ]
    
    df['abnormality_count'] = df[abnormality_cols].sum(axis=1)
    abnormality_count_table = df['abnormality_count'].value_counts().sort_index()
    combo_counts = df[abnormality_cols].value_counts().sort_values(ascending=False)
    normal_cols = ['Normal bmi', 'Normal systolic pressure', 'Normal glucose', 'Normal haemoglobin']
    normal_combo_counts = df[normal_cols].value_counts().sort_values(ascending=False)
    
    return abnormality_count_table, combo_counts, normal_combo_counts, df[abnormality_cols], df

def plot_correlation_heatmap(df, title="Correlation Between Abnormal Metrics"):
    """Generate an annotated correlation plot instead of a dense heatmap."""
    import numpy as np
    df = df.apply(pd.to_numeric, errors='coerce')  # force numeric
    corr = df.corr().fillna(0)



    fig, ax = plt.subplots(figsize=(6, 6))
    scatter = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    # Show all ticks and label them
    ax.set_xticks(range(len(corr)))
    ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)

    # Annotate each cell with value
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                    ha="center", va="center",
                    color="black", fontsize=9)

    fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title(title, fontsize=14)
    plt.tight_layout()
    return fig


def main():
    st.set_page_config(page_title="Health Metrics Visualizer", page_icon="🏥", layout="wide")
    st.title("🏥 Health Metrics Visualizer")
    st.markdown("Upload your raw health data CSV to analyze metrics and abnormality patterns.")
    
    # Sidebar thresholds
    st.sidebar.header("Health Thresholds")
    bmi_lb = st.sidebar.number_input("BMI Lower Bound", value=18.5, min_value=10.0, max_value=50.0, step=0.1)
    bmi_ub = st.sidebar.number_input("BMI Upper Bound", value=24.9, min_value=10.0, max_value=50.0, step=0.1)
    press_lb = st.sidebar.number_input("Systolic Pressure Lower Bound", value=90, min_value=50, max_value=200, step=1)
    press_ub = st.sidebar.number_input("Systolic Pressure Upper Bound", value=120, min_value=50, max_value=200, step=1)
    haem_lb = st.sidebar.number_input("Haemoglobin Lower Bound", value=12.0, min_value=5.0, max_value=20.0, step=0.1)
    haem_ub = st.sidebar.number_input("Haemoglobin Upper Bound", value=15.0, min_value=5.0, max_value=20.0, step=0.1)
    glu_ub = st.sidebar.number_input("Glucose Upper Bound", value=140.0, min_value=50.0, max_value=300.0, step=1.0)
    
    with st.expander("📋 Expected Data Format"):
        st.markdown("""
        Your CSV should contain these columns:
        - **v445**: BMI values
        - **sb18s, sb25s, sb29s**: Three systolic pressure readings
        - **v453**: Haemoglobin values  
        - **sb74**: Glucose values
        """)
    
    # Upload file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            pdf = pd.read_csv(uploaded_file)
            st.success(f"✅ Successfully loaded CSV with {len(pdf)} rows and {len(pdf.columns)} columns")
            
            with st.expander("📊 Raw Data Preview"):
                st.dataframe(pdf.head())
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Available Columns:**")
                    st.write(list(pdf.columns))
                with col2:
                    st.write("**Data Types:**")
                    st.write(pdf.dtypes.to_dict())
            
            # Analyse button
            analyse_btn = st.button("🔍 Analyse Data")
            
            if analyse_btn:
                with st.spinner("Processing health data..."):
                    df = process_raw_data(pdf, bmi_lb, bmi_ub, press_lb, press_ub, haem_lb, haem_ub, glu_ub)
                if df is None:
                    st.stop()
                
                st.success("✅ Health indicators created successfully!")
                
                # Processed data summary
                with st.expander("📈 Processed Data Summary"):
                    col1, col2, col3, col4 = st.columns(4)
                    normal_bmi = df['Normal bmi'].sum()
                    st.metric("Normal BMI", f"{normal_bmi}/{len(df)}", f"{100*normal_bmi/len(df):.1f}%")
                    normal_bp = df['Normal systolic pressure'].sum()
                    st.metric("Normal BP", f"{normal_bp}/{len(df)}", f"{100*normal_bp/len(df):.1f}%")
                    normal_hb = df['Normal haemoglobin'].sum()
                    st.metric("Normal Hb", f"{normal_hb}/{len(df)}", f"{100*normal_hb/len(df):.1f}%")
                    normal_glucose = df['Normal glucose'].sum()
                    st.metric("Normal Glucose", f"{normal_glucose}/{len(df)}", f"{100*normal_glucose/len(df):.1f}%")
                    
                    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
                    axes[0,0].hist(df['BMI_value'].dropna(), bins=30, alpha=0.7, color='skyblue')
                    axes[0,0].axvline(bmi_lb, color='red', linestyle='--')
                    axes[0,0].axvline(bmi_ub, color='red', linestyle='--')
                    axes[0,0].set_title('BMI Distribution')
                    
                    axes[0,1].hist(df['Systolic_value'].dropna(), bins=30, alpha=0.7, color='lightgreen')
                    axes[0,1].axvline(press_lb, color='red', linestyle='--')
                    axes[0,1].axvline(press_ub, color='red', linestyle='--')
                    axes[0,1].set_title('Systolic Pressure Distribution')
                    
                    axes[1,0].hist(df['Haemoglobin_value'].dropna(), bins=30, alpha=0.7, color='lightcoral')
                    axes[1,0].axvline(haem_lb, color='red', linestyle='--')
                    axes[1,0].axvline(haem_ub, color='red', linestyle='--')
                    axes[1,0].set_title('Haemoglobin Distribution')
                    
                    axes[1,1].hist(df['Glucose_value'].dropna(), bins=30, alpha=0.7, color='gold')
                    axes[1,1].axvline(glu_ub, color='red', linestyle='--')
                    axes[1,1].set_title('Glucose Distribution')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                
                # Abnormality analysis
                abnormality_count_table, combo_counts, normal_combo_counts, ab_df, processed_df = analyze_health_data(df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Abnormality Count Distribution")
                    fig1, ax1 = plt.subplots(figsize=(8, 6))
                    abnormality_count_table.plot(kind="bar", ax=ax1, color="skyblue")
                    ax1.set_xlabel("Number of Abnormalities")
                    ax1.set_ylabel("Number of People")
                    st.pyplot(fig1)
                    st.dataframe(abnormality_count_table.to_frame(name="Count"))
                
                with col2:
                    st.subheader("Correlation Between Abnormal Metrics")
                    fig2 = plot_correlation_heatmap(ab_df)
                    st.pyplot(fig2)
                
                st.header("📋 Detailed Combinations")
                tab1, tab2, tab3 = st.tabs(["Top Abnormal Combinations", "Top Normal Combinations", "Individual Records"])
                with tab1:
                    st.dataframe(combo_counts.head(10).to_frame(name="Count"))
                with tab2:
                    st.dataframe(normal_combo_counts.head(10).to_frame(name="Count"))
                with tab3:
                    display_df = processed_df[['Normal bmi', 'Normal systolic pressure', 'Normal haemoglobin', 
                                                'Normal glucose', 'abnormality_count', 'BMI_value', 'Systolic_value', 
                                                'Haemoglobin_value', 'Glucose_value']].head(20)
                    st.dataframe(display_df)
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
    
    else:
        st.info("👆 Please upload a CSV file to begin analysis")
        st.subheader("Expected Raw Data Format")
        example_data = {
            'v445': [22.5, 28.3, 19.1, 31.2],
            'sb18s': [115, 140, 95, 160], 
            'sb25s': [118, 142, 98, 158],
            'sb29s': [120, 138, 100, 162],
            'v453': [13.2, 11.8, 14.5, 10.2],
            'sb74': [95, 180, 88, 210]
        }
        st.dataframe(pd.DataFrame(example_data))

if __name__ == "__main__":
    main()