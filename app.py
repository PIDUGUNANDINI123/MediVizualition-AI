import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Page config
st.set_page_config(page_title="MedViz AI", layout="wide")

# Sidebar style
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0f172a;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏥 MedViz AI")
menu = st.sidebar.radio("Navigation", [
    "Upload Data",
    "Visualization",
    "Prediction",
    "Insights",
    "NLP Query"
])

# Store data
if "data" not in st.session_state:
    st.session_state.data = None

# ==============================
# 🔹 1. UPLOAD DATA
# ==============================
if menu == "Upload Data":
    st.title("📤 Upload Healthcare Data")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.session_state.data = df

        st.success("Data uploaded successfully!")
        st.dataframe(df)

# ==============================
# 🔹 2. VISUALIZATION (SMART FIXED)
# ==============================
elif menu == "Visualization":
    st.title("📊 Smart Visualization")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Detect column types
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        # Remove ID-like columns
        filtered_cols = [col for col in df.columns if "id" not in col.lower()]

        col = st.selectbox("Select Column", filtered_cols)
        chart = st.selectbox("Chart Type", [
            "Bar",
            "Countplot",
            "Pie",
            "Histogram",
            "Line"
        ])

        fig, ax = plt.subplots(figsize=(8, 5))

        # 🚫 Block ID columns
        if "id" in col.lower():
            st.error("ID columns are not suitable for visualization ❌")

        else:
            unique_vals = df[col].nunique()

            # ----------------------
            # 📊 BAR / COUNTPLOT
            # ----------------------
            if chart in ["Bar", "Countplot"]:
                if unique_vals > 20:
                    st.warning("Too many categories — showing top 10 only")
                    data = df[col].value_counts().nlargest(10)
                else:
                    data = df[col].value_counts()

                sns.barplot(x=data.index, y=data.values, ax=ax)
                ax.set_title(f"{chart} of {col}")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

            # ----------------------
            # 🥧 PIE
            # ----------------------
            elif chart == "Pie":
                if unique_vals <= 5:
                    df[col].value_counts().plot(
                        kind='pie',
                        autopct='%1.1f%%',
                        ax=ax
                    )
                    ax.set_ylabel("")
                else:
                    st.warning("Pie chart only works for ≤ 5 categories")

            # ----------------------
            # 📉 HISTOGRAM
            # ----------------------
            elif chart == "Histogram":
                if col in numeric_cols:
                    sns.histplot(df[col], kde=True, ax=ax)
                else:
                    st.warning("Histogram only works for numeric data")

            # ----------------------
            # 📈 LINE
            # ----------------------
            elif chart == "Line":
                if col in numeric_cols:
                    df[col].reset_index(drop=True).plot(ax=ax)
                else:
                    st.warning("Line chart works best for numeric trends")

            st.pyplot(fig)

            # ----------------------
            # 📥 Download chart
            # ----------------------
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)

            st.download_button(
                label="📥 Download Chart",
                data=buf,
                file_name=f"{chart}_{col}.png",
                mime="image/png"
            )

    else:
        st.warning("Upload data first!")

# ==============================
# 🔹 3. PREDICTION
# ==============================
elif menu == "Prediction":
    st.title("🤖 AI Disease Risk Prediction")

    age = st.number_input("Age", 1, 100)
    sugar = st.number_input("Sugar Level", 50, 300)
    gender = st.selectbox("Gender", ["Male", "Female"])

    if st.button("Predict Risk"):
        if age > 50 or sugar > 180:
            st.error("High Risk ⚠️")
        elif age > 30:
            st.warning("Medium Risk ⚡")
        else:
            st.success("Low Risk ✅")

# ==============================
# 🔹 4. INSIGHTS
# ==============================
elif menu == "Insights":
    st.title("📈 Automated Insights")

    if st.session_state.data is not None:
        df = st.session_state.data

        if "Age" in df.columns:
            st.info(f"Average Age: {int(df['Age'].mean())}")

        if "Disease" in df.columns:
            common = df["Disease"].value_counts().idxmax()
            st.success(f"Most common disease: {common}")

        if "SugarLevel" in df.columns:
            avg = df["SugarLevel"].mean()
            if avg > 140:
                st.warning(f"High avg sugar: {int(avg)}")
            else:
                st.success(f"Normal avg sugar: {int(avg)}")

        if "Gender" in df.columns:
            st.write(df["Gender"].value_counts())

    else:
        st.warning("Upload data first!")

# ==============================
# 🔹 5. NLP QUERY
# ==============================
elif menu == "NLP Query":
    st.title("💬 NLP Query System")

    if st.session_state.data is not None:
        df = st.session_state.data

        query = st.text_input("Ask something about data")

        if st.button("Run Query"):
            q = query.lower()

            if "disease" in q:
                fig, ax = plt.subplots()
                sns.countplot(x=df["Disease"], ax=ax)
                st.pyplot(fig)

            elif "age" in q:
                fig, ax = plt.subplots()
                sns.histplot(df["Age"], kde=True, ax=ax)
                st.pyplot(fig)

            elif "gender" in q:
                st.write(df["Gender"].value_counts())

            elif "sugar" in q:
                fig, ax = plt.subplots()
                sns.histplot(df["SugarLevel"], kde=True, ax=ax)
                st.pyplot(fig)

            else:
                st.warning("Try: age, disease, sugar, gender")

    else:
        st.warning("Upload data first!")
