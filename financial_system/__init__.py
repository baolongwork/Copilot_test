"""
Financial System Package
A simple financial transaction processing system for testing purposes.
"""

__version__ = "1.0.0"
__author__ = "Financial Systems Team"

from .processor import TransactionProcessor, Transaction, Account, process_large_transfer
from .constants import (
    SECURITY_ENFORCED,
    LARGE_TRANSACTION_THRESHOLD,
    TRANSACTION_COMPLETED,
)

__all__ = [
    "TransactionProcessor",
    "Transaction",
    "Account",
    "process_large_transfer",
    "SECURITY_ENFORCED",
    "LARGE_TRANSACTION_THRESHOLD",
    "TRANSACTION_COMPLETED",
]
