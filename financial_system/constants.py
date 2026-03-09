"""
Global constants for the financial transaction processing system.
"""

# Security Configuration
SECURITY_ENFORCED = True

# Transaction limits (in USD)
MINIMUM_TRANSACTION_AMOUNT = 0.01
MAXIMUM_DAILY_TRANSACTION = 100000.00

# Account types
ACCOUNT_TYPE_CHECKING = "CHECKING"
ACCOUNT_TYPE_SAVINGS = "SAVINGS"
ACCOUNT_TYPE_MONEY_MARKET = "MONEY_MARKET"

# Transaction status codes
TRANSACTION_PENDING = "PENDING"
TRANSACTION_COMPLETED = "COMPLETED"
TRANSACTION_FAILED = "FAILED"
TRANSACTION_REVERSED = "REVERSED"

# Error codes
ERROR_INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
ERROR_INVALID_ACCOUNT = "INVALID_ACCOUNT"
ERROR_TRANSACTION_LIMIT_EXCEEDED = "TRANSACTION_LIMIT_EXCEEDED"
ERROR_SECURITY_VIOLATION = "SECURITY_VIOLATION"

# ================================================================================
# INVARIANT RULE: Every transaction over 10,000 USD must have an accompanying 
# audit_log field; otherwise it will be considered a security violation.
# 
# This is a critical security requirement that must be enforced across all
# transaction processing functions. Violation of this rule results in
# immediate security failure.
# ================================================================================

LARGE_TRANSACTION_THRESHOLD = 10000.00

# Audit levels
AUDIT_LEVEL_BASIC = "BASIC"
AUDIT_LEVEL_DETAILED = "DETAILED"
AUDIT_LEVEL_CRITICAL = "CRITICAL"

# Database connection defaults
DB_RECONNECT_ATTEMPTS = 5
DB_RECONNECT_DELAY = 2  # seconds
DB_TIMEOUT = 30  # seconds

# Rate limiting
MAX_TRANSACTIONS_PER_MINUTE = 60
MAX_API_CALLS_PER_HOUR = 10000

# Timezone for transactions
DEFAULT_TIMEZONE = "UTC"

# Currency codes
CURRENCY_USD = "USD"
CURRENCY_EUR = "EUR"
CURRENCY_GBP = "GBP"

# Notification settings
NOTIFICATION_EMAIL_ON_LARGE_TRANSACTION = True
NOTIFICATION_SMS_THRESHOLD = 5000.00

# API response codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500
