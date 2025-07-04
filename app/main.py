import streamlit as st

from cyclingdb.data.loader import load_riders_data
from cyclingdb.search.engine import RiderSearchEngine

# Column name mappings for tooltips
COLUMN_TOOLTIPS = {
    "Name": "Rider Name",
    "Team": "Team Name",
    "Age": "Age",
    "Eval": "Evaluation",
    "FL": "Flat",
    "MO": "Mountain",
    "HL": "Hill",
    "BA": "Baroudeur",
    "DH": "Downhill",
    "CS": "Cobblestones",
    "TT": "Time Trial",
    "PR": "Prologue",
    "SP": "Sprint",
    "AC": "Acceleration",
    "ST": "Stamina",
    "RS": "Resistance",
    "RC": "Recovery",
}


def create_styled_dataframe(df):
    """Create a styled dataframe with column tooltips."""
    # Create column configuration for st.dataframe
    column_config = {}

    # Define numeric stat columns (for special formatting)
    stat_columns = [
        "FL",
        "MO",
        "HL",
        "BA",
        "DH",
        "CS",
        "TT",
        "PR",
        "SP",
        "AC",
        "ST",
        "RS",
        "RC",
    ]

    for col in df.columns:
        if col in COLUMN_TOOLTIPS:
            if col in stat_columns:
                # Style numeric stat columns with progress bar (PCM range: 50-85)
                column_config[col] = st.column_config.ProgressColumn(
                    label=col,
                    help=COLUMN_TOOLTIPS[col],
                    min_value=50,
                    max_value=85,
                    format="%d",
                )
            elif col == "Age":
                # Style age column as number
                column_config[col] = st.column_config.NumberColumn(
                    label=col, help=COLUMN_TOOLTIPS[col], format="%d"
                )
            else:
                # Regular text columns
                column_config[col] = st.column_config.Column(
                    label=col, help=COLUMN_TOOLTIPS[col]
                )

    return column_config


# Page configuration
st.set_page_config(
    page_title="CyclingDB - PCM25 Rider Database",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Title
st.title("🚴 CyclingDB - Pro Cycling Manager 25 Rider Database")

# Load the rider data
try:
    riders_df = load_riders_data()
    search_engine = RiderSearchEngine(riders_df)

    # Get overall statistics
    overall_stats = search_engine.get_stats()

except Exception as e:
    st.error(f"Failed to load rider data: {str(e)}")
    st.stop()

# Search and Filters Section
st.header("Search & Filters")

# Search box
search_term = st.text_input("Search riders by name", placeholder="Enter rider name...")

# Filter options in a clean layout
filter_row1_col1, filter_row1_col2, filter_row1_col3, filter_row1_col4 = st.columns(4)

with filter_row1_col1:
    # Get unique teams for dropdown
    unique_teams = search_engine.get_unique_values("Team")
    team_filter = st.multiselect("Team", options=unique_teams)

with filter_row1_col2:
    specialization = st.selectbox(
        "Specialization",
        options=["", "mountain", "sprint", "time trial", "classics", "overall"],
        index=0,
    )

with filter_row1_col3:
    # Get age range from database
    age_min = int(riders_df["Age"].min()) if "Age" in riders_df.columns else 16
    age_max = int(riders_df["Age"].max()) if "Age" in riders_df.columns else 50
    age_range = st.slider(
        "Age Range", min_value=age_min, max_value=age_max, value=(age_min, age_max)
    )
    min_age, max_age = age_range
    # Only filter if not using full range
    if (min_age, max_age) == (age_min, age_max):
        min_age = max_age = None

with filter_row1_col4:
    st.write("")  # Empty since age is now a single range slider

# Second row for overall rating filters
filter_row2_col1, filter_row2_col2, filter_row2_col3, filter_row2_col4 = st.columns(4)

with filter_row2_col1:
    # Use the calculated Eval column for overall rating filtering
    if "Eval" in riders_df.columns:
        overall_min = int(riders_df["Eval"].min())
        overall_max = int(riders_df["Eval"].max())

        # Check if we have a valid range
        if overall_min < overall_max:
            overall_range = st.slider(
                "Overall Rating (Eval)",
                min_value=overall_min,
                max_value=overall_max,
                value=(overall_min, overall_max),
            )
            min_overall, max_overall = overall_range
            # Only filter if not using full range
            if (min_overall, max_overall) == (overall_min, overall_max):
                min_overall = max_overall = None
        else:
            # All values are the same, no point in filtering
            min_overall = max_overall = None
            st.info(f"All riders have the same Eval rating ({overall_min})")
    else:
        # No Eval column found, disable overall filtering
        min_overall = max_overall = None
        st.info("No Eval column found")

with filter_row2_col2:
    st.write("")  # Empty since overall is now a single range slider

with filter_row2_col3:
    st.write("")  # Reserved for future filter

with filter_row2_col4:
    st.write("")  # Reserved for future filter

# Perform search
filtered_df = search_engine.search(
    name_query=search_term if search_term else None,
    team=team_filter if team_filter else None,
    min_age=min_age,
    max_age=max_age,
    min_overall=min_overall,
    max_overall=max_overall,
    specialization=specialization if specialization else None,
)

# Get filtered statistics
filtered_stats = search_engine.get_stats(filtered_df)

st.markdown("---")

# Statistics Section
st.header("Statistics")

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric("Total Riders", f"{overall_stats['total_riders']:,}")
with stats_col2:
    st.metric("Teams", f"{overall_stats['teams']:,}")
with stats_col3:
    st.metric("Average Age", f"{overall_stats['avg_age']:.1f}")
with stats_col4:
    st.metric("Filtered", f"{filtered_stats['total_riders']:,}")

st.markdown("---")

# Data Table Section
st.header("Riders")

if len(filtered_df) > 0:
    # Create column configuration with tooltips
    column_config = create_styled_dataframe(filtered_df)

    # Display the filtered data with tooltips
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )

    # Download button for filtered results
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label=f"Download Filtered Results ({len(filtered_df)} riders)",
        data=csv_data,
        file_name="filtered_riders.csv",
        mime="text/csv",
    )

    # Show column info
    with st.expander("Column Information"):
        st.write("**Available Columns:**")
        for col in filtered_df.columns:
            st.write(f"- {col}")

else:
    st.warning(
        "No riders match the current filters. Try adjusting your search criteria."
    )

# Footer
st.markdown("---")
st.markdown(
    "💡 **Tip**: Use the search and filters above to find specific riders. Click on a row to see full details."
)
