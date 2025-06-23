# Pro Cycling Manager 25 Database Search App

A lekker Streamlit web app to search and filter the PCM25 rider database with styled data display.

## Core Requirements
- Auto-download CSV from: https://web.cyanide-studio.com/games/cycling/2025/pcm/riders/?export=csv
- Main app: `app/main.py`
- Package: `cyclingdb` in `src/cyclingdb/`
- Dependencies: UV package manager

## Features Built
- **Name search**: Partial matching, case-insensitive
- **Team filter**: Multiselect dropdown with real team names
- **Age/Rating filters**: Min/max ranges for age and overall stats
- **Specialization filter**: Mountain, sprint, time trial, etc.
- **Styled dataframe**: Progress bars for stats, tooltips on hover
- **CSV export**: Download filtered results
- **Real-time stats**: Total riders, teams, average age, filtered count

## Data Structure
- **900 riders** across various teams
- **Columns**: Name, Team, Age, Eval, FL, MO, HL, BA, DH, CS, TT, PR, SP, AC, ST, RS, RC
- **CSV format**: Semicolon-delimited, UTF-8/Latin-1 encoding
- **Stats tooltips**: FL=Flat, MO=Mountain, TT=Time Trial, SP=Sprint, etc.

## Architecture
- `src/cyclingdb/data/loader.py`: Auto-download, cache with @st.cache_data
- `src/cyclingdb/search/engine.py`: Pandas filtering with boolean indexing
- `app/main.py`: Layout: Title → Filters → Stats → Styled Table

## Development Workflow
- **Git Integration**: Work closely with git and GitHub for all development
- **Issue Management**: Create GitHub issues for new features/bugs using `gh issue create`
- **Branch Management**: Checkout feature branches for issues using `gh issue develop <issue#>`
- **Code Quality**: Format with `uv run ruff format .` and check with `uv run ruff check .`
- **Testing**: Run app with `uv run streamlit run app/main.py`
- **Commits**: Use clear, descriptive commit messages referencing issues with "Fixes #N"
- **Package Imports**: Use proper package imports (no path hacking)
- **Pull Requests**: Create PRs for feature branches and reference related issues