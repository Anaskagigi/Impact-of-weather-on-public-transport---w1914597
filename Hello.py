import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Weather & Public Transport Analysis", layout="wide")

# Load data with caching for performance optimization
@st.cache_data
def load_data():
    df = pd.read_csv('data/5_Years_Weather_Impact_on_Public_Transport.csv')
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is in datetime format
    df.fillna(0, inplace=True)  # Handle missing values
    return df

# Load the data
df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
transport_modes = df['Transport Mode'].unique()
selected_mode = st.sidebar.multiselect("Select Transport Mode(s)", transport_modes, default=transport_modes)

weather_conditions = df['Weather Condition'].unique()
selected_weather = st.sidebar.multiselect("Select Weather Condition(s)", weather_conditions, default=weather_conditions)

# Year Range Slider
min_year, max_year = df['Date'].dt.year.min(), df['Date'].dt.year.max()
year_range = st.sidebar.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Apply Filters
filtered_df = df[(df['Transport Mode'].isin(selected_mode)) &
                 (df['Weather Condition'].isin(selected_weather)) &
                 (df['Date'].dt.year.between(year_range[0], year_range[1]))]

# Display KPIs
st.title("📊 Weather Impact on Public Transport")
st.markdown("### Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

col1.metric("Total Delays (min)", filtered_df['Delay Due to Weather (minutes)'].sum())
col2.metric("Average Delay (min)", round(filtered_df['Delay Due to Weather (minutes)'].mean(), 2))
col3.metric("Number of Affected Trips", filtered_df.shape[0])

# Data Visualization
st.markdown("---")
st.subheader("📈 Delay Trends Over Time")
time_fig = px.line(filtered_df, x='Date', y='Delay Due to Weather (minutes)', color='Transport Mode', title="Delays Over Time")
st.plotly_chart(time_fig, use_container_width=True)

st.subheader("🚆 Delays by Transport Mode")
mode_fig = px.bar(filtered_df, x='Transport Mode', y='Delay Due to Weather (minutes)', color='Weather Condition',
                  title="Total Delay by Transport Mode", barmode='group')
st.plotly_chart(mode_fig, use_container_width=True)

st.subheader("🌦️ Weather Impact on Delays")
weather_fig = px.box(filtered_df, x='Weather Condition', y='Delay Due to Weather (minutes)', color='Transport Mode',
                     title="Weather Condition vs Delay")
st.plotly_chart(weather_fig, use_container_width=True)

# Conclusion
with st.expander("📌 Conclusion"):
    st.write("This analysis shows how different weather conditions affect public transport delays.")
    st.write("- Extreme weather increases delays significantly.")
    st.write("- Some transport modes are more resilient than others.")
    st.write("Further analysis can help optimize scheduling during adverse weather conditions.")

# Feedback Section
with st.expander("💬 Feedback"):
    feedback = st.text_area("Let us know your thoughts!")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Display Raw Data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
