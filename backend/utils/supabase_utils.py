# supabase_utils.py
from ..db.database import get_supabase_client

async def execute_query(table_name, query_type, data=None, filters=None):
    """Execute a query on Supabase
    
    Args:
        table_name (str): The name of the table to query
        query_type (str): The type of query to execute (select, insert, update, delete)
        data (dict, optional): The data to insert or update. Defaults to None.
        filters (dict, optional): The filters to apply to the query. Defaults to None.
        
    Returns:
        dict: The response from Supabase
    """
    supabase = get_supabase_client()
    
    if query_type == "select":
        query = supabase.table(table_name).select("*")
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
                
        response = query.execute()
        return response.data
    
    elif query_type == "insert":
        response = supabase.table(table_name).insert(data).execute()
        return response.data
    
    elif query_type == "update":
        query = supabase.table(table_name).update(data)
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
                
        response = query.execute()
        return response.data
    
    elif query_type == "delete":
        query = supabase.table(table_name)
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
                
        response = query.delete().execute()
        return response.data
    
    else:
        raise ValueError(f"Invalid query type: {query_type}")