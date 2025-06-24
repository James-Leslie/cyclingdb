# CyclingDB - Pro Cycling Manager 25 Rider Database

A Streamlit web application for searching and filtering the Pro Cycling Manager 25 rider database.

## Features

- **Search & Filter**: Find riders by name, nationality, team, age, and specialization
- **Interactive Table**: View rider stats with sortable columns
- **Export Data**: Download filtered results as CSV
- **Real-time Stats**: See count of riders, countries, and teams

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/James-Leslie/cyclingdb.git
cd cyclingdb
```

2. Install dependencies:
```bash
uv sync
```

3. Run the application:
```bash
streamlit run app/main.py
```

4. Open your browser to `http://localhost:8501`

### Development

The app will automatically download the PCM25 rider database on first run. For development:

```bash
# Install in editable mode
uv pip install -e .

# Run the app
streamlit run app/main.py
```

## Project Structure

```
cyclingdb/
├── app/
│   └── main.py              # Main Streamlit application
├── src/cyclingdb/
│   ├── data/
│   │   └── loader.py        # Data loading and caching
│   └── search/
│       └── engine.py        # Search and filtering logic
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## CDB File Tools

For working with Pro Cycling Manager CDB database files directly:

- **Full Editor V4**: https://pcmdaily.com/infusions/pro_download_panel/download.php?did=907
  - Contains `PCM2008_CDB_to_XML.exe` for converting CDB files to XML format
  - Useful for extracting data from game installation files

## Contributing

1. Make changes to the code
2. Test with `streamlit run app/main.py`
3. Commit changes to git
4. Submit pull request