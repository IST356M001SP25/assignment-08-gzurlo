import pandas as pd

def top_locations(violations_df: pd.DataFrame, threshold=1000):
    """
    Return a dataframe of locations with $1,000 or more in total fines.
    Columns: location, amount
    Should have 135 rows.
    """
    # Group by location and sum the amounts
    top_locs = violations_df.groupby('location')['amount'].sum().reset_index()
    
    # Filter locations meeting the threshold
    top_locs = top_locs[top_locs['amount'] >= threshold]
    
    # Sort by amount descending
    top_locs = top_locs.sort_values('amount', ascending=False)
    
    return top_locs

def top_locations_mappable(violations_df: pd.DataFrame, threshold=1000):
    """
    Get top locations with lat/lon added.
    Columns: location, lat, lon, amount
    Should have same row count as top_locations.
    """
    # Get the top locations
    top_locs = top_locations(violations_df, threshold)
    
    # Get first occurrence of each location to get its coordinates
    loc_coords = violations_df.drop_duplicates('location')[['location', 'lat', 'lon']]
    
    # Merge to add coordinates
    top_locs_mappable = pd.merge(top_locs, loc_coords, on='location', how='left')
    
    return top_locs_mappable

def tickets_in_top_locations(violations_df: pd.DataFrame, threshold=1000):
    """
    Return tickets issued in top locations.
    Should have 8,109 rows.
    """
    # Get list of top locations
    top_locs = top_locations(violations_df, threshold)['location']
    
    # Filter original dataframe
    top_tickets = violations_df[violations_df['location'].isin(top_locs)]
    
    return top_tickets

if __name__ == '__main__':
    # Read input data
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    
    # Process data
    top_locs_df = top_locations(violations_df)
    top_locs_mappable_df = top_locations_mappable(violations_df)
    top_tickets_df = tickets_in_top_locations(violations_df)
    
    # Write outputs
    top_locs_df.to_csv('./cache/top_locations.csv', index=False)
    top_locs_mappable_df.to_csv('./cache/top_locations_mappable.csv', index=False)
    top_tickets_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)