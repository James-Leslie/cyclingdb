import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CyclingDB - PCM25 Rider Database", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🚴 CyclingDB - Pro Cycling Manager 25 Rider Database")

# Sidebar for search and filters
with st.sidebar:
    st.header("Search & Filters")
    
    # Search box
    search_term = st.text_input("Search riders by name", placeholder="Enter rider name...")
    
    # Filters (placeholder for now)
    st.subheader("Filters")
    nationality_filter = st.text_input("Nationality", placeholder="e.g. France")
    team_filter = st.text_input("Team", placeholder="e.g. Team UAE")
    
    # Age range
    col1, col2 = st.columns(2)
    with col1:
        min_age = st.number_input("Min Age", min_value=16, max_value=50, value=20)
    with col2:
        max_age = st.number_input("Max Age", min_value=16, max_value=50, value=40)
    
    # Apply filters button
    apply_filters = st.button("Apply Filters", type="primary")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
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

with col2:
    st.header("Statistics")
    
    # Placeholder stats
    st.metric("Total Riders", "0")
    st.metric("Countries", "0")
    st.metric("Teams", "0")
    
    # Instructions
    st.subheader("Next Steps")
    st.markdown("""
    1. Implement data loader
    2. Add search functionality 
    3. Implement filters
    4. Add rider detail view
    """)

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Use the sidebar to search and filter riders. Click on a row to see full details.")