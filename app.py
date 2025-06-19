import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from joblib import load
import plotly.graph_objects as go

st.set_page_config(page_title="Jaya Jaya Institute Dashboard", layout="wide")

# Load and process data
data = pd.read_csv("databaru.csv", delimiter=",")
data_0 = data.loc[data['Status']==0]
data_1 = data.loc[data['Status']==1]
data_2 = data.loc[data['Status']==2]

category_mapping = {
    33: 'Biofuel Production Technologies',
    171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)',
    9003: 'Agronomy',
    9070: 'Communication Design',
    9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering',
    9130: 'Equinculture',
    9147: 'Management',
    9238: 'Social Service',
    9254: 'Tourism',
    9500: 'Nursing',
    9556: 'Oral Hygiene',
    9670: 'Advertising and Marketing Management',
    9773: 'Journalism and Communication',
    9853: 'Basic Education',
    9991: 'Management (evening attendance)'
}
data['Course_Label'] = data['Course'].replace(category_mapping)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    add_selectbox = st.selectbox(
        "Choose a page",
        ("Dashboard", "Prediction"),
        index=0
    )

# CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 25px 20px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-title {
        font-size: 13px;
        color: #6c757d;
        margin-bottom: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #212529;
        line-height: 1;
    }
    .dropout-rate {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .dropout-rate-title {
        font-size: 18px;
        margin-bottom: 15px;
        font-weight: 500;
    }
    .dropout-rate-value {
        font-size: 42px;
        font-weight: bold;
        line-height: 1;
    }
    .section-header {
        background: linear-gradient(90deg, #f1f3f4, #e8f0fe);
        padding: 20px;
        border-radius: 10px;
        margin: 25px 0 15px 0;
        border-left: 5px solid #4285f4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .section-header h3 {
        margin: 0;
        color: #1a73e8;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def create_metric_card(title, value, color="#4285f4"):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
    </div>
    """

def create_pie_chart(column, title):
    try:
        value_counts = kelas[column].value_counts()
        if len(value_counts) > 1:
            names = [False, True]
        else:
            if value_counts.index[0] == 1:
                names = [True]
            elif value_counts.index[0] == 0:
                names = [False]
        
        colors = ['#ff6b6b', '#4285f4']
        fig = px.pie(
            values=value_counts,
            names=names,
            title=title,
            color_discrete_sequence=colors
        )
        fig.update_layout(
            height=200,
            margin=dict(l=10, r=10, t=50, b=40),
            title=dict(
                x=0.5,
                font=dict(size=12),
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5
            )
        )
        return fig
    except Exception as e:
        return None

if add_selectbox == "Dashboard":
    # Header
    st.title('🎓 Jaya Institute Student Performance Dashboard')
    st.markdown("**Author:** Dwi Hadi Yulvi Baskoro / @hadhibaskoro")
    st.markdown("---")
    
    # Filters Section
    st.markdown('<div class="section-header"><h3>📊 Filters</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_list = ['None', 'Dropout', 'Not Dropout']
        selected_status = st.selectbox('📋 Select Status', status_list, key='initial_status')
        
        if selected_status == 'Dropout':
            selected_status = 0
        elif selected_status == 'Not Dropout':
            st.session_state['split_columns'] = True
            status_list = ['None', 'Enrolled', 'Graduated']
            selected_status = st.selectbox('📚 Select Type of Not Dropout', status_list, key='not_dropout_type')
            if selected_status == 'None':
                selected_status = 'Not Dropout'
            elif selected_status == 'Enrolled':
                selected_status = 1
            elif selected_status == 'Graduated':
                selected_status = 2

    with col2:
        course_list = list(data.Course_Label.unique())
        course_list.sort()
        course_list.insert(0, "None")
        selected_course = st.selectbox('🎯 Select Course', course_list)

    with col3:
        time_list = ['None', 'Daytime', 'Evening']
        selected_time = st.selectbox('⏰ Select Attendance Time', time_list)
        if selected_time == 'Daytime':
            selected_time = 1
        elif selected_time == 'Evening':
            selected_time = 0

    with col4:
        gender_list = ['None', 'Male', 'Female']
        selected_gender = st.selectbox('👥 Select Gender', gender_list)
        if selected_gender == 'Male':
            selected_gender = 1
        elif selected_gender == 'Female':
            selected_gender = 0
    
    # Apply filters
    if selected_status == 'None':
        kelas = data
    elif selected_status == 'Not Dropout':
        kelas = data.loc[data['Status_New'] == 1]
    else:
        kelas = data.loc[data['Status'] == selected_status]

    if selected_course != "None":
        kelas = kelas.loc[kelas['Course_Label'] == selected_course]

    if selected_time != "None":
        kelas = kelas.loc[kelas['Daytime_evening_attendance'] == selected_time]

    if selected_gender != "None":
        kelas = kelas.loc[kelas['Gender'] == selected_gender]

    st.markdown("---")
    
    # Key Metrics Section
    st.markdown('<div class="section-header"><h3>📈 Key Metrics</h3></div>', unsafe_allow_html=True)
    
    # Calculate metrics
    total_students = kelas['Status_0'].sum() + kelas['Status_1'].sum() + kelas['Status_2'].sum()
    dropout_students = kelas['Status_0'].sum()
    enrolled_students = kelas['Status_1'].sum()
    graduated_students = kelas['Status_2'].sum()
    
    if total_students > 0:
        dropout_rate = round((dropout_students / total_students) * 100, 2)
        enrolled_rate = round((enrolled_students / total_students) * 100, 2)
        graduation_rate = round((graduated_students / total_students) * 100, 2)
    else:
        dropout_rate = enrolled_rate = graduation_rate = 0
    
    # Metrics display
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"""
        <div class="dropout-rate">
            <div class="dropout-rate-title">🚨 Dropout Rate</div>
            <div class="dropout-rate-value">{dropout_rate}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.markdown(create_metric_card("Total Students", f"{total_students:,}", "#4285f4"), unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown(create_metric_card("Dropped Out", f"{dropout_students:,}", "#ff6b6b"), unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown(create_metric_card("Enrolled", f"{enrolled_students:,}", "#34a853"), unsafe_allow_html=True)
        
        with metric_col4:
            st.markdown(create_metric_card("Graduated", f"{graduated_students:,}", "#fbbc04"), unsafe_allow_html=True)

    st.markdown("---")
    
    # Charts Section
    st.markdown('<div class="section-header"><h3>📊 Analysis Charts</h3></div>', unsafe_allow_html=True)
    
    # First row of charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader('🎓 Scholarship Holders by Status')
        
        if selected_status == "None":
            grouper = "Status"
        elif selected_status == 'Not Dropout':
            grouper = "Status_New"
        else:
            grouper = "Status_" + str(selected_status)
        
        try:
            a = kelas.groupby(grouper)['Scholarship_holder'].sum()
            if not a.empty:
                maxA = a.idxmax()
                colors = ['#e8f0fe' if b != maxA else '#4285f4' for b in a.index]
                
                fig = px.bar(
                    x=a.index, 
                    y=a, 
                    title="Scholarship Holders by Status",
                    color=a.index,
                    color_discrete_sequence=colors
                )
                fig.update_traces(text=a.values, textposition='outside')
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    xaxis_title="Status",
                    yaxis_title="Number of Students"
                )
                
                if grouper == 'Status':
                    fig.update_xaxes(tickvals=a.index, ticktext=['Dropout', 'Enrolled', 'Graduated'])
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")
        except Exception as e:
            st.error("Unable to display chart due to insufficient data.")
    
    with chart_col2:
        st.subheader('📚 Average Grades per Semester')
        
        try:
            avg_1st_sem = kelas.groupby(grouper)['Curricular_units_1st_sem_grade'].mean()
            avg_2nd_sem = kelas.groupby(grouper)['Curricular_units_2nd_sem_grade'].mean()
            
            if not avg_1st_sem.empty and not avg_2nd_sem.empty:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='1st Semester',
                    x=avg_1st_sem.index,
                    y=avg_1st_sem.values,
                    marker_color='#4285f4',
                    text=[f"{value:.2f}" for value in avg_1st_sem.values],
                    textposition='auto'
                ))
                
                fig.add_trace(go.Bar(
                    name='2nd Semester',
                    x=avg_2nd_sem.index,
                    y=avg_2nd_sem.values,
                    marker_color='#34a853',
                    text=[f"{value:.2f}" for value in avg_2nd_sem.values],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    title="Average Grades per Semester",
                    xaxis_title="Status",
                    yaxis_title="Average Grade",
                    barmode='group',
                    height=400
                )
                
                if grouper == 'Status':
                    fig.update_xaxes(tickvals=avg_1st_sem.index, ticktext=['Dropout', 'Enrolled', 'Graduated'])
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")
        except Exception as e:
            st.error("Unable to display chart due to insufficient data.")
    
    # Second row - Course Analysis
    st.markdown("---")
    st.markdown('<div class="section-header"><h3>📋 Course Analysis & Student Characteristics</h3></div>', unsafe_allow_html=True)
    
    chart_col3, chart_col4 = st.columns([2.5, 1])
    
    with chart_col3:
        st.subheader("📋 Dropout Rate by Course")
        
        try:
            course_kls = kelas.copy()
            course_kls['Course'] = course_kls['Course'].map(category_mapping)
            
            data_do = course_kls[course_kls['Status_0'] == 1]
            data_notdo = course_kls.loc[course_kls['Status'] > 0]
            
            course_do = data_do.groupby('Course')['Status_0'].sum()
            course_notdo = data_notdo.groupby('Course')['Status_New'].sum()
            
            if not course_do.empty and not course_notdo.empty:
                total_course = round((course_do / (course_do + course_notdo) * 100), 2)
                a_sorted = total_course.sort_values()
                
                fig = px.bar(
                    x=a_sorted.values,
                    y=a_sorted.index,
                    orientation='h',
                    title="Dropout Rate by Course",
                    color=a_sorted.values,
                    color_continuous_scale='Reds'
                )
                fig.update_traces(text=[f"{value}%" for value in a_sorted.values], textposition='outside')
                fig.update_layout(
                    height=500,
                    xaxis_title="Dropout Rate (%)",
                    yaxis_title="Course",
                    showlegend=False,
                    margin=dict(l=20, r=80, t=60, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")
        except Exception as e:
            st.error("Unable to display chart due to insufficient data.")
    
    with chart_col4:
        st.subheader("🔍 Student Characteristics")
        
        # Educational Special Needs
        fig1 = create_pie_chart('Educational_special_needs', 'Educational Special Needs')
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        
        # Debtor Distribution
        fig2 = create_pie_chart('Debtor', 'Debtor Distribution')
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
        
        # Tuition Fees
        fig3 = create_pie_chart('Tuition_fees_up_to_date', 'Tuition Fees Up to Date')
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
    
    # Third row - Age Analysis
    st.markdown("---")
    st.markdown('<div class="section-header"><h3>👥 Age Demographics</h3></div>', unsafe_allow_html=True)
    
    age_col1, age_col2 = st.columns([2.5, 1])
    
    with age_col1:
        st.subheader("👥 Age at Enrollment Distribution")
        
        try:
            if not kelas.empty:
                fig = px.histogram(
                    kelas,
                    x='Age_at_enrollment',
                    nbins=20,
                    title='Age at Enrollment Distribution',
                    color_discrete_sequence=['#4285f4']
                )
                fig.update_layout(
                    height=350,
                    xaxis_title="Age at Enrollment",
                    yaxis_title="Number of Students",
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")
        except Exception as e:
            st.error("Unable to display chart due to insufficient data.")
    
    with age_col2:
        st.subheader("📊 Age Statistics")
        
        if not kelas.empty:
            min_age = int(kelas['Age_at_enrollment'].min())
            mean_age = round(kelas['Age_at_enrollment'].mean(), 1)
            max_age = int(kelas['Age_at_enrollment'].max())
            
            st.markdown(create_metric_card("Minimum Age", f"{min_age} years", "#ff6b6b"), unsafe_allow_html=True)
            st.markdown(create_metric_card("Average Age", f"{mean_age} years", "#4285f4"), unsafe_allow_html=True)
            st.markdown(create_metric_card("Maximum Age", f"{max_age} years", "#34a853"), unsafe_allow_html=True)
        else:
            st.info("No age data available for the selected filters.")

elif add_selectbox == "Prediction":
    st.title("🔮 Student Dropout Prediction")
    st.markdown("Fill in the student information below to predict dropout risk.")
    st.markdown("---")
    
    # Prediction form
    with st.form("prediction_form"):
        st.subheader("📋 Student Information")
        
        # Course selection
        course_list = list(data.Course_Label.unique())
        course_list.sort()
        course_selected = st.selectbox('🎯 Course', course_list, key='pred_course')
        
        # Convert to numeric
        reverse_mapping = {v: k for k, v in category_mapping.items()}
        course_numeric = reverse_mapping[course_selected]
        
        # Determine time based on course
        if course_numeric in [9991, 8014]:
            time_selected = 0
            st.info("ℹ️ This course is offered in evening attendance only.")
        else:
            time_selected = 1
            st.info("ℹ️ This course is offered in daytime attendance.")
        
        # Student details
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Personal Information")
            gender_selected = st.selectbox('Gender', ['Male', 'Female'])
            gender_numeric = 1 if gender_selected == "Male" else 0
            
            age_selected = st.number_input("Age at enrollment", min_value=17, max_value=70, value=20)
            
            admgrade_selected = st.number_input("Admission grade", min_value=0.0, max_value=200.0, value=120.0, step=0.1)
        
        with col2:
            st.subheader("🎓 Academic & Financial")
            special_selected = st.radio('Educational special needs?', ['No', 'Yes'])
            special_numeric = 1 if special_selected == "Yes" else 0
            
            debtor_selected = st.radio('Debtor?', ['No', 'Yes'])
            debtor_numeric = 1 if debtor_selected == "Yes" else 0
            
            tuition_selected = st.radio('Tuition fees up to date?', ['Yes', 'No'])
            tuition_numeric = 1 if tuition_selected == "Yes" else 0
            
            scholarship_selected = st.radio('Scholarship holder?', ['No', 'Yes'])
            scholarship_numeric = 1 if scholarship_selected == "Yes" else 0
        
        # Grades
        st.subheader("📊 Academic Performance")
        grade_col1, grade_col2 = st.columns(2)
        
        with grade_col1:
            grade1_selected = st.number_input("First semester grade", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
        
        with grade_col2:
            grade2_selected = st.number_input("Second semester grade", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
        
        # Prediction button
        submitted = st.form_submit_button("🔍 Predict Dropout Risk", type="primary")
        
        if submitted:
            try:
                model = load('model.joblib')
                
                user_data = {
                    'Course': [course_numeric], 
                    'Daytime_evening_attendance': [time_selected], 
                    'Admission_grade': [admgrade_selected], 
                    'Educational_special_needs': [special_numeric], 
                    'Debtor': [debtor_numeric], 
                    'Tuition_fees_up_to_date': [tuition_numeric], 
                    'Gender': [gender_numeric], 
                    'Scholarship_holder': [scholarship_numeric], 
                    'Age_at_enrollment': [age_selected], 
                    'Curricular_units_1st_sem_grade': [grade1_selected],
                    'Curricular_units_2nd_sem_grade': [grade2_selected]
                }

                X_new = pd.DataFrame(user_data)
                predictions = model.predict(X_new)
                
                st.markdown("---")
                st.subheader("🎯 Prediction Result")
                
                if predictions[0] == 0:
                    st.error("⚠️ **HIGH RISK**: Student is likely to dropout.")
                    st.markdown("""
                    **Recommendations:**
                    - Provide additional academic support
                    - Consider mentoring programs
                    - Monitor attendance closely
                    - Offer financial counseling if needed
                    """)
                else:
                    st.success("✅ **LOW RISK**: Student is NOT likely to dropout.")
                    st.markdown("""
                    **Recommendations:**
                    - Continue current support level
                    - Encourage participation in extracurricular activities
                    - Maintain regular check-ins
                    """)
                    
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
                st.info("Please ensure all fields are filled correctly and the model file is available.")