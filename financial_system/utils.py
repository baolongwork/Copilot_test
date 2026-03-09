"""
Utility functions for string and time manipulation in the financial system.
This module provides helper functions for processing transaction data and formatting.
"""

import re
from datetime import datetime, timedelta, timezone
from typing import List, Tuple, Optional, Dict
import hashlib


def format_currency(amount: float, currency_code: str = "USD", decimals: int = 2) -> str:
    """
    Format an amount as a currency string with proper formatting and symbols.
    
    Args:
        amount: The numeric amount to format
        currency_code: Three-letter currency code (default: USD)
        decimals: Number of decimal places (default: 2)
    
    Returns:
        Formatted currency string
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
    }
    symbol = currency_symbols.get(currency_code, currency_code)
    formatted_amount = f"{amount:,.{decimals}f}"
    return f"{symbol}{formatted_amount}"


def validate_account_number(account_number: str) -> bool:
    """
    Validate account number format using regex pattern matching.
    Account numbers should be 10-16 alphanumeric characters.
    
    Args:
        account_number: The account number to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[A-Z0-9]{10,16}$"
    return bool(re.match(pattern, account_number))


def validate_routing_number(routing_number: str) -> bool:
    """
    Validate US routing number (9-digit number).
    
    Args:
        routing_number: The routing number to validate
    
    Returns:
        True if valid format, False otherwise
    """
    if not re.match(r"^\d{9}$", routing_number):
        return False
    return True


def parse_transaction_description(description: str) -> Dict[str, str]:
    """
    Parse a transaction description string into components.
    Expected format: "TYPE:MERCHANT:LOCATION:CATEGORY"
    
    Args:
        description: Transaction description string
    
    Returns:
        Dictionary with parsed components
    """
    parts = description.split(":")
    return {
        "type": parts[0].strip() if len(parts) > 0 else "",
        "merchant": parts[1].strip() if len(parts) > 1 else "",
        "location": parts[2].strip() if len(parts) > 2 else "",
        "category": parts[3].strip() if len(parts) > 3 else "",
    }


def normalize_phone_number(phone_number: str) -> Optional[str]:
    """
    Normalize a phone number by removing non-digit characters.
    Only keeps digit characters.
    
    Args:
        phone_number: The phone number to normalize
    
    Returns:
        Normalized phone number or None if empty after normalization
    """
    normalized = re.sub(r"\D", "", phone_number)
    return normalized if normalized else None


def sanitize_transaction_reference(reference: str) -> str:
    """
    Sanitize transaction reference by removing dangerous characters.
    Keeps only alphanumeric, hyphens, and underscores.
    
    Args:
        reference: The reference string to sanitize
    
    Returns:
        Sanitized reference string
    """
    return re.sub(r"[^a-zA-Z0-9_-]", "", reference)


def get_current_timestamp(include_timezone: bool = True) -> str:
    """
    Get the current timestamp in ISO format.
    
    Args:
        include_timezone: Whether to include timezone information
    
    Returns:
        ISO formatted timestamp string
    """
    if include_timezone:
        return datetime.now(timezone.utc).isoformat()
    else:
        return datetime.now().isoformat()


def parse_iso_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Parse an ISO format timestamp string into a datetime object.
    
    Args:
        timestamp_str: ISO formatted timestamp string
    
    Returns:
        datetime object or None if parsing fails
    """
    try:
        return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def calculate_transaction_duration(start_time: str, end_time: str) -> Optional[float]:
    """
    Calculate the duration between two ISO timestamps in seconds.
    
    Args:
        start_time: ISO formatted start timestamp
        end_time: ISO formatted end timestamp
    
    Returns:
        Duration in seconds or None if parsing fails
    """
    start = parse_iso_timestamp(start_time)
    end = parse_iso_timestamp(end_time)
    
    if start and end:
        return (end - start).total_seconds()
    return None


def generate_transaction_id(length: int = 32) -> str:
    """
    Generate a unique transaction ID using current timestamp and hash.
    
    Args:
        length: Desired length of the transaction ID
    
    Returns:
        Generated transaction ID
    """
    timestamp = datetime.now().isoformat().encode()
    hash_obj = hashlib.sha256(timestamp)
    hex_dig = hash_obj.hexdigest()
    return hex_dig[:length]


def format_iso_date(date_obj: datetime) -> str:
    """
    Format a datetime object as ISO date string (YYYY-MM-DD).
    
    Args:
        date_obj: datetime object to format
    
    Returns:
        ISO formatted date string
    """
    return date_obj.strftime("%Y-%m-%d")


def get_week_start_and_end(date_obj: datetime) -> Tuple[str, str]:
    """
    Get the start and end dates of the week for a given date.
    Week starts on Monday.
    
    Args:
        date_obj: datetime object
    
    Returns:
        Tuple of (start_date, end_date) in ISO format
    """
    start = date_obj - timedelta(days=date_obj.weekday())
    end = start + timedelta(days=6)
    return format_iso_date(start), format_iso_date(end)


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length and add suffix if truncated.
    
    Args:
        text: String to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def extract_merchant_name(transaction_string: str) -> str:
    """
    Extract merchant name from a transaction string using pattern matching.
    
    Args:
        transaction_string: Transaction description
    
    Returns:
        Extracted merchant name
    """
    match = re.search(r"MERCHANT:\s*([A-Za-z0-9\s]+)", transaction_string)
    return match.group(1).strip() if match else "Unknown"


def validate_email(email: str) -> bool:
    """
    Validate email address using regex pattern.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
