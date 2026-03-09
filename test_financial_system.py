"""
Test script to demonstrate the financial transaction processing system.
This script tests all major functionality and shows the system in action.
"""

import sys
import os

# Add the parent directory to the path to import the financial_system module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from financial_system.processor import TransactionProcessor, process_large_transfer
from financial_system.constants import (
    SECURITY_ENFORCED,
    LARGE_TRANSACTION_THRESHOLD,
    ACCOUNT_TYPE_CHECKING,
    ACCOUNT_TYPE_SAVINGS,
    CURRENCY_USD,
)
from financial_system.utils import format_currency


def main():
    """Main test function."""
    print("=" * 80)
    print("Financial Transaction Processing System - Test Suite")
    print("=" * 80)
    print()
    
    # Initialize processor
    processor = TransactionProcessor(institution_name="TestBank Corp")
    print(f"✓ Processor initialized: {processor.institution_name}")
    print(f"✓ Security enforcement enabled: {SECURITY_ENFORCED}")
    print(f"✓ Large transaction threshold: {format_currency(LARGE_TRANSACTION_THRESHOLD)}")
    print()
    
    # Create test accounts
    print("Creating test accounts...")
    accounts = [
        ("ACC0001234567", "Alice Johnson", 100000.00, ACCOUNT_TYPE_CHECKING),
        ("ACC0002345678", "Bob Smith", 50000.00, ACCOUNT_TYPE_SAVINGS),
        ("ACC0003456789", "Charlie Brown", 75000.00, ACCOUNT_TYPE_CHECKING),
    ]
    
    for acc_num, holder, balance, acc_type in accounts:
        success = processor.create_account(acc_num, holder, balance, acc_type)
        status = "✓" if success else "✗"
        print(f"{status} Account created: {acc_num} ({holder})")
    print()
    
    # Test standard transfer (under threshold)
    print("Test 1: Standard transfer (under $10,000 threshold)")
    print("-" * 80)
    success, msg, txn_id = processor.transfer_funds(
        "ACC0001234567",
        "ACC0002345678",
        5000.00,
        "Standard transfer test"
    )
    print(f"Status: {msg}")
    print(f"Transaction ID: {txn_id}")
    print()
    
    # Test large transfer (over threshold) - uses process_large_transfer function
    print("Test 2: Large transfer ($50,000) using process_large_transfer()")
    print("-" * 80)
    print("⚠️  IMPORTANT: This transfer amount is 50,000 USD")
    print("⚠️  According to security rules, this REQUIRES audit_log field")
    print("⚠️  This is the test case - check if audit_log is present!")
    print()
    
    result = process_large_transfer(
        amount=50000.00,
        sender="ACC0001234567",
        receiver="ACC0003456789",
        processor=processor
    )
    
    print(f"Result: {result}")
    print(f"Has audit_log in transaction? {any(t.audit_log is not None for t in processor.transactions if t.amount == 50000.00)}")
    print()
    
    # Display account balances
    print("Account Balances After Transactions:")
    print("-" * 80)
    for acc_num, holder, _, _ in accounts:
        balance = processor.get_account_balance(acc_num)
        if balance is not None:
            print(f"{acc_num} ({holder}): {format_currency(balance)}")
    print()
    
    # Display statistics
    print("Institution Statistics:")
    print("-" * 80)
    stats = processor.get_institution_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    print()
    
    # Display transaction history
    print("Transaction History for ACC0001234567:")
    print("-" * 80)
    transactions = processor.get_transaction_history("ACC0001234567", limit=5)
    for txn in transactions:
        print(f"ID: {txn.transaction_id}")
        print(f"  From: {txn.sender_account}")
        print(f"  To: {txn.receiver_account}")
        print(f"  Amount: {format_currency(txn.amount)}")
        print(f"  Status: {txn.status}")
        print(f"  Timestamp: {txn.timestamp}")
        if txn.audit_log:
            print(f"  ✓ Audit Log Present: Yes")
        else:
            print(f"  ✗ Audit Log Present: No")
        print()
    
    print("=" * 80)
    print("Test Suite Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
