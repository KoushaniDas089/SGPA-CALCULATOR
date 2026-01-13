import streamlit as st

# 1. Page Configuration, Custom CSS
st.set_page_config(page_title="SGPA Analyzer", page_icon="📝")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background-color: #2e7d32; 
        color: white; 
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    /* result area */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("SGPA Analyzer")
st.write("A simple tool to calculate Semester Grade Point Average based on course credits.")

# 2. Grade Mapping

grade_map = {"O": 10, "E": 9, "A": 8, "B": 7, "C": 6, "D": 5, "F": 0}

# 3. Input: no. of subjects
num_subs = st.number_input("Enter the number of subjects:", 
                           min_value=1, max_value=20, value=5)

# 4. The Entry Form

with st.form("marks_form"):
    st.info("Fill in the Subject Name, Credits, and Grade received:")
    
    # Storing inputs in these lists to calculate them after clicking 'Submit'
    subject_data = []

    for i in range(int(num_subs)):
        cols = st.columns([3, 1, 1])
        
        with cols[0]:
            name = st.text_input(f"Subject {i+1}", placeholder="e.g. Data Structures", key=f"name_{i}")
        with cols[1]:
            # Credits input
            cred = st.number_input("Credits", min_value=1.0, max_value=10.0, value=3.0, step=0.5, key=f"cred_{i}")
        with cols[2]:
            grade = st.selectbox("Grade", list(grade_map.keys()), key=f"grade_{i}")
        
        # Store the data for calculation later
        subject_data.append({"credits": cred, "grade": grade})
        
    # The Submit Button
    submitted = st.form_submit_button("Calculate Final SGPA")

# 5. Calculation and Result Display
if submitted:
    total_points = 0
    total_credits = 0
    has_failed = False

    for item in subject_data:
        # Calculate points: Grade Value * Subject Credits
        grade_value = grade_map[item["grade"]]
        total_points += grade_value * item["credits"]
        total_credits += item["credits"]
        
        # Check for 'F' grade
        if item["grade"] == "F":
            has_failed = True

    # Final Result Calculation
    if total_credits > 0:
        sgpa = total_points / total_credits
        
        st.divider()
        st.metric(label="Your SGPA", value=f"{sgpa:.2f}")

        # feedback based on SGPA
        if has_failed:
            st.error("Result: Backlog/Fail.")
        elif sgpa >= 9.0:
            st.success("Result: Outstanding!")
            st.balloons()
        elif sgpa >= 7.5:
            st.info("Result: Great job.")
        elif sgpa >= 6.0:
            st.info("Result: Satisfactory.")
    else:
        st.error("Invalid input for credits.")
