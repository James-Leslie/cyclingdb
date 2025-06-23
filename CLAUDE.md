# Pro Cycling Manager 25 Database Search App

Build a Streamlit web app to search the PCM25 rider database.

## Core Requirements
- Download CSV from: https://web.cyanide-studio.com/games/cycling/2025/pcm/riders/?export=csv
- Main app file: `app/main.py`
- Package name: `cyclingdb` in `src/cyclingdb/`
- Use UV for dependency management

## Key Features

### Search & Filters
- Text search by rider name (partial matching, case-insensitive)
- Filter by: nationality, team, age range, specialisation, rating ranges
- Multiple filters should combine (AND logic)
- Sort results by any column

### Data Display
- Results table with key columns visible
- Click row to see full rider details
- Export filtered results as CSV
- Show result count and basic statistics

## Implementation Details

### Data Loading (`src/cyclingdb/data/loader.py`)
```python
@st.cache_data
def load_riders_data():
    # Check if data/riders.csv exists
    # If not, download from URL using requests
    # Load with pandas (try UTF-8, fallback to Latin-1)
    # Return DataFrame
```

### Search Engine (`src/cyclingdb/search/engine.py`)
- Use pandas string methods for text search
- Apply filters using boolean indexing
- Return filtered DataFrame

### Streamlit App (`app/streamlit_app.py`)
- Sidebar: search box + all filters
- Main area: results table using `st.dataframe()`
- Use `st.columns()` for layout
- Add download button: `st.download_button()`
- Handle empty results gracefully

## CSV Handling
- The CSV likely has Latin-1 encoding
- Column names may have spaces - strip them
- Expect columns like: Name, Nationality, Team, Age, Mountain, Sprint, Time Trial, Overall
- Inspect the actual CSV structure first

## Streamlit Tips
- Use `st.sidebar` for all inputs
- Cache expensive operations with `@st.cache_data`
- Use `st.empty()` for loading states
- Set page config: `st.set_page_config(page_title="PCM25 Database", layout="wide")`

## Error Handling
- Wrap CSV download in try/except
- Show user-friendly error messages
- Provide retry button if download fails
- Validate CSV has expected columns

## Performance
- Only load full CSV once per session
- Use DataFrame views, not copies
- Limit displayed rows with pagination if >1000 results

## Deployment
- Ensure CSV is in `.gitignore` if large
- For Streamlit Cloud: download CSV on first run
- Set appropriate `client.maxUploadSize` in `.streamlit/config.toml` if needed

## Development Workflow
- All changes MUST be committed to git
- After each significant change, commit the work
- Present commits to user for review before proceeding
- Use clear, descriptive commit messages