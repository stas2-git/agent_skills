"""
Utility functions for Excel tool execution
"""

from datetime import datetime

def convert_value_type(value):
    """
    Intelligently convert string values to appropriate types.
    Prevents "Number Stored as Text" errors in Excel.
    
    Args:
        value: Value to convert (typically string from JSON)
        
    Returns:
        Converted value (int, float, bool, or original string)
        
    Examples:
        >>> convert_value_type("50000")
        50000
        >>> convert_value_type("123.45")
        123.45
        >>> convert_value_type("=A1+B1")
        '=A1+B1'
        >>> convert_value_type("Revenue")
        'Revenue'
    """
    # If already not a string, return as-is
    if not isinstance(value, str):
        return value
    
    # Preserve formulas as strings
    if value.startswith('='):
        return value
    
    # Try date conversion (handles "12/31/19", "2019-12-31", etc.)
    # Must come before numeric conversion to avoid parsing "1/2" as 0.5
    if '/' in value or '-' in value:
        try:
            # Try common date formats
            for fmt in ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']:
                try:
                    dt = datetime.strptime(value, fmt)
                    # Convert to Excel date serial number (days since 1900-01-01)
                    # Excel epoch is 1899-12-30 (accounting for Excel's 1900 leap year bug)
                    excel_epoch = datetime(1899, 12, 30)
                    delta = dt - excel_epoch
                    return delta.days + (delta.seconds / 86400.0)
                except ValueError:
                    continue
        except Exception:
            pass
    
    # Try integer conversion (handles "50000", "-123", etc.)
    try:
        # Check if it's a clean integer (no decimal point)
        if '.' not in value and 'e' not in value.lower():
            return int(value)
    except (ValueError, AttributeError):
        pass
    
    # Try float conversion (handles "123.45", "1.5e10", etc.)
    try:
        return float(value)
    except (ValueError, AttributeError):
        pass
    
    # Boolean conversion
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    
    # Return original string if no conversion works
    return value

