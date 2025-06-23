import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CyclingDB - PCM25 Rider Database", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title
st.title("🚴 CyclingDB - Pro Cycling Manager 25 Rider Database")

# Search and Filters Section
st.header("Search & Filters")

# Search box
search_term = st.text_input("Search riders by name", placeholder="Enter rider name...")

# Filters in columns
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    nationality_filter = st.text_input("Nationality", placeholder="e.g. France")

with filter_col2:
    team_filter = st.text_input("Team", placeholder="e.g. Team UAE")

with filter_col3:
    min_age = st.number_input("Min Age", min_value=16, max_value=50, value=20)

with filter_col4:
    max_age = st.number_input("Max Age", min_value=16, max_value=50, value=40)

# Apply filters button
apply_filters = st.button("Apply Filters", type="primary")

st.markdown("---")

# Statistics Section
st.header("Statistics")

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric("Total Riders", "0")
with stats_col2:
    st.metric("Countries", "0")
with stats_col3:
    st.metric("Teams", "0")
with stats_col4:
    st.metric("Filtered", "0")

st.markdown("---")

# Data Table Section
st.header("Riders")

# Placeholder for data table
if st.button("Load Sample Data"):
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'Name': ['John Doe', 'Jane Smith', 'Pierre Dubois'],
        'Nationality': ['USA', 'GBR', 'FRA'],
        'Team': ['Team A', 'Team B', 'Team C'],
        'Age': [25, 28, 32],
        'Overall': [75, 82, 68],
        'Mountain': [70, 85, 60],
        'Sprint': [80, 65, 75]
    })
    
    st.dataframe(
        sample_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    st.download_button(
        label="Download CSV",
        data=sample_data.to_csv(index=False),
        file_name="filtered_riders.csv",
        mime="text/csv"
    )
else:
    st.info("Click 'Load Sample Data' to see the interface in action, or implement the data loader to load real PCM25 data.")

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Use the search and filters above to find specific riders. Click on a row to see full details.")