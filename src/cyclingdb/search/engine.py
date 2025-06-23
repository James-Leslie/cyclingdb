"""Search and filtering engine for rider data."""

import pandas as pd
from typing import Optional, Dict, Any


class RiderSearchEngine:
    """Search engine for filtering and searching rider data."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize the search engine with rider data.
        
        Args:
            df: DataFrame containing rider data
        """
        self.df = df.copy()
    
    def search(
        self,
        name_query: Optional[str] = None,
        nationality: Optional[str] = None,
        team: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        min_overall: Optional[int] = None,
        max_overall: Optional[int] = None,
        specialization: Optional[str] = None
    ) -> pd.DataFrame:
        """Search and filter riders based on criteria.
        
        Args:
            name_query: Partial name search (case-insensitive)
            nationality: Filter by nationality
            team: Filter by team name
            min_age: Minimum age
            max_age: Maximum age
            min_overall: Minimum overall rating
            max_overall: Maximum overall rating
            specialization: Filter by specialization type
            
        Returns:
            pd.DataFrame: Filtered results
        """
        result_df = self.df.copy()
        
        # Text search by name (partial matching, case-insensitive)
        if name_query and name_query.strip():
            if 'Name' in result_df.columns:
                mask = result_df['Name'].str.contains(
                    name_query.strip(),
                    case=False,
                    na=False
                )
                result_df = result_df[mask]
        
        # Filter by nationality
        if nationality and nationality.strip():
            if 'Nationality' in result_df.columns:
                mask = result_df['Nationality'].str.contains(
                    nationality.strip(),
                    case=False,
                    na=False
                )
                result_df = result_df[mask]
        
        # Filter by team
        if team and team.strip():
            if 'Team' in result_df.columns:
                mask = result_df['Team'].str.contains(
                    team.strip(),
                    case=False,
                    na=False
                )
                result_df = result_df[mask]
        
        # Age range filter
        if 'Age' in result_df.columns:
            if min_age is not None:
                result_df = result_df[result_df['Age'] >= min_age]
            if max_age is not None:
                result_df = result_df[result_df['Age'] <= max_age]
        
        # Overall rating filter
        if 'Overall' in result_df.columns:
            if min_overall is not None:
                result_df = result_df[result_df['Overall'] >= min_overall]
            if max_overall is not None:
                result_df = result_df[result_df['Overall'] <= max_overall]
        
        # Specialization filter (find highest stat)
        if specialization and specialization.strip():
            specialization = specialization.strip().lower()
            result_df = self._filter_by_specialization(result_df, specialization)
        
        return result_df
    
    def _filter_by_specialization(self, df: pd.DataFrame, specialization: str) -> pd.DataFrame:
        """Filter riders by their specialization (highest stat).
        
        Args:
            df: DataFrame to filter
            specialization: Type of specialization ('mountain', 'sprint', 'time trial', 'classics', etc.)
            
        Returns:
            pd.DataFrame: Filtered DataFrame
        """
        # Define stat columns that might exist
        stat_columns = []
        for col in df.columns:
            col_lower = col.lower()
            if any(stat in col_lower for stat in ['mountain', 'sprint', 'time trial', 'overall', 'classics']):
                stat_columns.append(col)
        
        if not stat_columns:
            return df  # No stat columns found, return as is
        
        # Map specialization terms to column names
        spec_mapping = {
            'mountain': ['mountain', 'climber', 'hill'],
            'sprint': ['sprint', 'flat'],
            'time trial': ['time trial', 'tt', 'chrono'],
            'classics': ['classics', 'cobbles'],
            'overall': ['overall', 'general classification', 'gc']
        }
        
        # Find matching columns for the specialization
        target_columns = []
        for key, terms in spec_mapping.items():
            if specialization in terms:
                for col in stat_columns:
                    if any(term in col.lower() for term in terms):
                        target_columns.append(col)
                break
        
        if not target_columns:
            return df  # No matching specialization found
        
        # Filter riders where the specialization stat is their highest
        filtered_indices = []
        for idx, row in df.iterrows():
            stat_values = {}
            for col in stat_columns:
                try:
                    stat_values[col] = float(row[col])
                except (ValueError, TypeError):
                    stat_values[col] = 0
            
            if stat_values:
                max_stat = max(stat_values.values())
                # Check if any of the target columns has the max value
                for col in target_columns:
                    if stat_values.get(col, 0) == max_stat:
                        filtered_indices.append(idx)
                        break
        
        return df.loc[filtered_indices] if filtered_indices else df.iloc[0:0]  # Return empty if no matches
    
    def get_unique_values(self, column: str) -> list:
        """Get unique values from a column for filter options.
        
        Args:
            column: Column name
            
        Returns:
            list: Sorted list of unique values
        """
        if column not in self.df.columns:
            return []
        
        unique_values = self.df[column].dropna().unique()
        return sorted([str(val) for val in unique_values])
    
    def get_stats(self, filtered_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Get statistics for the dataset or filtered results.
        
        Args:
            filtered_df: Optional filtered DataFrame, uses full dataset if None
            
        Returns:
            dict: Statistics dictionary
        """
        df_to_analyze = filtered_df if filtered_df is not None else self.df
        
        stats = {
            'total_riders': len(df_to_analyze),
            'countries': df_to_analyze['Nationality'].nunique() if 'Nationality' in df_to_analyze.columns else 0,
            'teams': df_to_analyze['Team'].nunique() if 'Team' in df_to_analyze.columns else 0,
            'avg_age': df_to_analyze['Age'].mean() if 'Age' in df_to_analyze.columns else 0
        }
        
        return stats