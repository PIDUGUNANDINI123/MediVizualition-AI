import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Page config
st.set_page_config(page_title="MedViz AI", layout="wide")

# Custom CSS (Dark Sidebar)
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
# 🔹 2. VISUALIZATION (UPDATED)
# ==============================
elif menu == "Visualization":
    st.title("📊 Advanced Visualization")

    if st.session_state.data is not None:
        df = st.session_state.data

        col = st.selectbox("Select Column", df.columns)
        chart = st.selectbox("Chart Type", [
            "Bar",
            "Countplot",
            "Pie",
            "Histogram",
            "Line"
        ])

        fig, ax = plt.subplots(figsize=(8, 5))

        # Charts
        if chart == "Bar":
            df[col].value_counts().plot(kind='bar', ax=ax)
            ax.set_title(f"Bar Chart of {col}")

        elif chart == "Countplot":
            sns.countplot(x=df[col], ax=ax)
            ax.set_title(f"Countplot of {col}")

        elif chart == "Pie":
            df[col].value_counts().plot(
                kind='pie',
                autopct='%1.1f%%',
                ax=ax
            )
            ax.set_ylabel("")
            ax.set_title(f"Pie Chart of {col}")

        elif chart == "Histogram":
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(f"Histogram of {col}")

        elif chart == "Line":
            df[col].plot(kind='line', ax=ax)
            ax.set_title(f"Line Chart of {col}")

        st.pyplot(fig)

        # Download chart
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)

        st.download_button(
            label="📥 Download Chart as PNG",
            data=buf,
            file_name=f"{chart}_{col}.png",
            mime="image/png"
        )

        st.caption("Tip: Download the chart and share via WhatsApp, Email, or Reports.")

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
            avg = int(df["Age"].mean())
            st.info(f"Most patients are around age {avg}")

        if "Disease" in df.columns:
            common = df["Disease"].value_counts().idxmax()
            count = df["Disease"].value_counts().max()
            st.success(f"{common} is most common ({count} cases)")

        if "SugarLevel" in df.columns:
            avg_sugar = int(df["SugarLevel"].mean())
            if avg_sugar > 140:
                st.warning(f"Average sugar level is high ({avg_sugar}) ⚠️")
            else:
                st.success(f"Average sugar level is normal ({avg_sugar})")

        if "Gender" in df.columns:
            st.write("Gender Distribution:")
            st.write(df["Gender"].value_counts())

        st.markdown("### 📌 Summary")
        st.write("The dataset reveals key health patterns and trends useful for decision making.")

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

            if "diabetes" in q or "disease" in q:
                st.subheader("Disease Distribution")
                fig, ax = plt.subplots()
                sns.countplot(x=df["Disease"], ax=ax)
                st.pyplot(fig)

            elif "age" in q:
                st.subheader("Age Distribution")
                fig, ax = plt.subplots()
                sns.histplot(df["Age"], kde=True, ax=ax)
                st.pyplot(fig)

            elif "gender" in q:
                st.write(df["Gender"].value_counts())

            elif "sugar" in q:
                fig, ax = plt.subplots()
                sns.histplot(df["SugarLevel"], kde=True, ax=ax)
                st.pyplot(fig)

            elif "common" in q:
                st.write("Most common disease:", df["Disease"].value_counts().idxmax())

            else:
                st.warning("Try queries like: age, disease, sugar, gender")

    else:
        st.warning("Upload data first!")
