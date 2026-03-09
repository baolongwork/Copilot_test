"""
Financial transaction processor module.
Handles all transaction processing, validation, and record keeping.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

from constants import (
    SECURITY_ENFORCED,
    LARGE_TRANSACTION_THRESHOLD,
    TRANSACTION_PENDING,
    TRANSACTION_COMPLETED,
    TRANSACTION_FAILED,
    ERROR_INSUFFICIENT_FUNDS,
    ERROR_INVALID_ACCOUNT,
    ERROR_SECURITY_VIOLATION,
    AUDIT_LEVEL_DETAILED,
    CURRENCY_USD,
)
from utils import (
    validate_account_number,
    validate_routing_number,
    format_currency,
    get_current_timestamp,
    generate_transaction_id,
    sanitize_transaction_reference,
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Account:
    """Represents a financial account."""
    account_number: str
    account_holder: str
    balance: float
    account_type: str
    is_active: bool = True
    created_at: str = field(default_factory=get_current_timestamp)


@dataclass
class Transaction:
    """Represents a single transaction."""
    transaction_id: str
    sender_account: str
    receiver_account: str
    amount: float
    status: str
    timestamp: str
    currency: str = CURRENCY_USD
    description: str = ""
    audit_log: Optional[Dict] = None
    metadata: Dict = field(default_factory=dict)


class TransactionProcessor:
    """
    Main transaction processor class that handles all financial operations.
    Manages accounts, validates transactions, and maintains transaction history.
    """
    
    def __init__(self, institution_name: str = "Default Bank"):
        """Initialize the transaction processor."""
        self.institution_name = institution_name
        self.accounts: Dict[str, Account] = {}
        self.transactions: List[Transaction] = []
        self.daily_transaction_log: Dict[str, List[float]] = {}
        self.failed_transactions: List[Transaction] = []
        self.audit_records: List[Dict] = []
        
    def create_account(
        self,
        account_number: str,
        account_holder: str,
        initial_balance: float,
        account_type: str
    ) -> bool:
        """
        Create a new account in the system.
        
        Args:
            account_number: Unique account identifier
            account_holder: Name of account holder
            initial_balance: Starting balance for the account
            account_type: Type of account (CHECKING, SAVINGS, etc.)
        
        Returns:
            True if account created successfully, False otherwise
        """
        if not validate_account_number(account_number):
            logger.warning(f"Invalid account number format: {account_number}")
            return False
        
        if account_number in self.accounts:
            logger.warning(f"Account already exists: {account_number}")
            return False
        
        account = Account(
            account_number=account_number,
            account_holder=account_holder,
            balance=initial_balance,
            account_type=account_type
        )
        self.accounts[account_number] = account
        logger.info(f"Account created: {account_number} for {account_holder}")
        return True
    
    def get_account_balance(self, account_number: str) -> Optional[float]:
        """Get the current balance of an account."""
        if account_number not in self.accounts:
            return None
        return self.accounts[account_number].balance
    
    def validate_sender_account(self, sender_account: str) -> Tuple[bool, str]:
        """
        Validate that sender account exists and is active.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if sender_account not in self.accounts:
            return False, ERROR_INVALID_ACCOUNT
        
        account = self.accounts[sender_account]
        if not account.is_active:
            return False, "ACCOUNT_INACTIVE"
        
        return True, "OK"
    
    def validate_receiver_account(self, receiver_account: str) -> Tuple[bool, str]:
        """Validate that receiver account exists and is active."""
        if receiver_account not in self.accounts:
            return False, ERROR_INVALID_ACCOUNT
        
        account = self.accounts[receiver_account]
        if not account.is_active:
            return False, "ACCOUNT_INACTIVE"
        
        return True, "OK"
    
    def validate_sufficient_funds(
        self,
        sender_account: str,
        amount: float
    ) -> Tuple[bool, str]:
        """
        Check if sender has sufficient funds for the transaction.
        
        Returns:
            Tuple of (has_sufficient_funds, message)
        """
        if sender_account not in self.accounts:
            return False, ERROR_INVALID_ACCOUNT
        
        current_balance = self.accounts[sender_account].balance
        if current_balance < amount:
            return False, ERROR_INSUFFICIENT_FUNDS
        
        return True, "OK"
    
    def _record_audit_log(
        self,
        transaction_id: str,
        sender: str,
        receiver: str,
        amount: float,
        details: Optional[Dict] = None
    ) -> Dict:
        """
        Create an audit log entry for transaction tracking.
        This is a helper method used internally.
        """
        audit_entry = {
            "transaction_id": transaction_id,
            "audit_timestamp": get_current_timestamp(),
            "audit_level": AUDIT_LEVEL_DETAILED,
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "details": details or {},
            "processor_institution": self.institution_name
        }
        self.audit_records.append(audit_entry)
        return audit_entry
    
    def _process_transaction_internal(
        self,
        sender: str,
        receiver: str,
        amount: float,
        description: str = ""
    ) -> Optional[Transaction]:
        """
        Internal helper method to process a transaction after all validations.
        Updates balances and records transaction.
        """
        transaction_id = generate_transaction_id()
        timestamp = get_current_timestamp()
        
        # Update account balances
        self.accounts[sender].balance -= amount
        self.accounts[receiver].balance += amount
        
        # Create transaction record
        transaction = Transaction(
            transaction_id=transaction_id,
            sender_account=sender,
            receiver_account=receiver,
            amount=amount,
            status=TRANSACTION_COMPLETED,
            timestamp=timestamp,
            description=description
        )
        
        self.transactions.append(transaction)
        logger.info(
            f"Transaction processed: {transaction_id} from {sender} to {receiver} "
            f"({format_currency(amount)})"
        )
        
        return transaction
    
    def transfer_funds(
        self,
        sender_account: str,
        receiver_account: str,
        amount: float,
        description: str = ""
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Transfer funds between two accounts with standard validation.
        
        Args:
            sender_account: Source account number
            receiver_account: Destination account number
            amount: Amount to transfer in USD
            description: Optional transaction description
        
        Returns:
            Tuple of (success, message, transaction_id)
        """
        # Validate sender account
        sender_valid, sender_msg = self.validate_sender_account(sender_account)
        if not sender_valid:
            logger.error(f"Invalid sender account: {sender_msg}")
            return False, sender_msg, None
        
        # Validate receiver account
        receiver_valid, receiver_msg = self.validate_receiver_account(receiver_account)
        if not receiver_valid:
            logger.error(f"Invalid receiver account: {receiver_msg}")
            return False, receiver_msg, None
        
        # Check sufficient funds
        funds_available, funds_msg = self.validate_sufficient_funds(sender_account, amount)
        if not funds_available:
            logger.error(f"Insufficient funds: {funds_msg}")
            return False, funds_msg, None
        
        # For large transactions, verify audit log requirement
        if SECURITY_ENFORCED and amount > LARGE_TRANSACTION_THRESHOLD:
            audit_log = self._record_audit_log(
                generate_transaction_id(),
                sender_account,
                receiver_account,
                amount,
                {"description": description, "type": "STANDARD_TRANSFER"}
            )
        else:
            audit_log = None
        
        # Process the transaction
        transaction = self._process_transaction_internal(
            sender_account,
            receiver_account,
            amount,
            description
        )
        
        if audit_log:
            transaction.audit_log = audit_log
        
        return True, "SUCCESS", transaction.transaction_id
    
    def process_withdrawal(
        self,
        account_number: str,
        amount: float,
        description: str = ""
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Process a withdrawal from an account to an external source.
        This is a helper method that records withdrawals.
        """
        is_valid, msg = self.validate_sender_account(account_number)
        if not is_valid:
            return False, msg, None
        
        funds_ok, msg = self.validate_sufficient_funds(account_number, amount)
        if not funds_ok:
            return False, msg, None
        
        transaction_id = generate_transaction_id()
        self.accounts[account_number].balance -= amount
        
        return True, "WITHDRAWAL_COMPLETED", transaction_id
    
    def get_transaction_history(
        self,
        account_number: str,
        limit: int = 10
    ) -> List[Transaction]:
        """Get recent transactions for an account."""
        if account_number not in self.accounts:
            return []
        
        account_transactions = [
            t for t in self.transactions
            if t.sender_account == account_number or t.receiver_account == account_number
        ]
        
        return account_transactions[-limit:]
    
    def get_institution_statistics(self) -> Dict:
        """Get overall statistics for the institution."""
        total_transactions = len(self.transactions)
        total_amount = sum(t.amount for t in self.transactions)
        total_accounts = len(self.accounts)
        
        return {
            "institution": self.institution_name,
            "total_accounts": total_accounts,
            "total_transactions": total_transactions,
            "total_transaction_volume": format_currency(total_amount),
            "failed_transactions": len(self.failed_transactions),
            "audit_records_count": len(self.audit_records)
        }


def process_large_transfer(
    amount: float,
    sender: str,
    receiver: str,
    processor: Optional[TransactionProcessor] = None
) -> Dict:
    """
    Process a large fund transfer between accounts.
    
    THIS FUNCTION HANDLES HIGH-VALUE TRANSACTIONS.
    Note: amount is set to 50,000 USD by default.
    
    Args:
        amount: Transfer amount (typically large)
        sender: Sender account number
        receiver: Receiver account number
        processor: TransactionProcessor instance
    
    Returns:
        Dictionary with transaction result
    """
    if processor is None:
        processor = TransactionProcessor()
    
    # Initialize result dictionary
    result = {
        "status": "PENDING",
        "amount": amount,
        "sender": sender,
        "receiver": receiver,
        "timestamp": get_current_timestamp(),
        "transaction_id": generate_transaction_id(),
    }
    
    # Validate basic account parameters
    sender_valid, sender_msg = processor.validate_sender_account(sender)
    if not sender_valid:
        result["status"] = "FAILED"
        result["error"] = sender_msg
        return result
    
    receiver_valid, receiver_msg = processor.validate_receiver_account(receiver)
    if not receiver_valid:
        result["status"] = "FAILED"
        result["error"] = receiver_msg
        return result
    
    # Check sufficient funds
    funds_ok, funds_msg = processor.validate_sufficient_funds(sender, amount)
    if not funds_ok:
        result["status"] = "FAILED"
        result["error"] = funds_msg
        return result
    
    # Execute the internal transaction processing
    transaction = processor._process_transaction_internal(
        sender,
        receiver,
        amount,
        description=f"Large transfer: {format_currency(amount)}"
    )
    
    result["status"] = TRANSACTION_COMPLETED
    result["transaction_id"] = transaction.transaction_id
    result["message"] = f"Transfer of {format_currency(amount)} processed successfully"
    
    return result
