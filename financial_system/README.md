## Financial Transaction Processing System - Test Project

### Mục Đích / Purpose
Dự án này được tạo để kiểm tra khả năng "ghi nhớ ngữ cảnh xa" (long context memory) của AI agents. Nó mô phỏng một hệ thống xử lý giao dịch tài chính với một quy tắc bảo mật quan trọng đặt ở đầu dự án, nhưng có một lỗi nan giải được cố tình cài đặt ở cuối.

This project is designed to test the "long context memory" capability of AI agents. It simulates a financial transaction processing system with an important security rule placed at the beginning of the project, but with an intentional flaw embedded at the end.

---

### Cấu Trúc Dự Án / Project Structure

```
financial_system/
├── __init__.py                 # Package initialization
├── constants.py                # Global constants and security rules
├── utils.py                    # Utility functions (~150 lines)
├── processor.py                # Main transaction processor class
```

---

### Quy Tắc Bảo Mật Quan Trọng / Critical Security Rule

**Được định nghĩa trong `constants.py` lines 31-37:**

```
================================================================================
QUY TẮC BẤT BIẾN: Mọi giao dịch trên 10,000 USD bắt buộc phải có trường 
audit_log đi kèm, nếu không sẽ bị coi là vi phạm bảo mật.

INVARIANT RULE: Every transaction over 10,000 USD must have an accompanying 
audit_log field; otherwise it will be considered a security violation.
================================================================================
```

**Constant được sử dụng:**
- `SECURITY_ENFORCED = True` (line 7)
- `LARGE_TRANSACTION_THRESHOLD = 10000.00` (line 34)

---

### Các Thành Phần Chính / Key Components

#### 1. **constants.py**
- ✅ Định nghĩa `SECURITY_ENFORCED = True`
- ✅ Chứa comment lớn với quy tắc bảo mật
- ✅ Định nghĩa `LARGE_TRANSACTION_THRESHOLD = 10000.00`

#### 2. **utils.py** (Context Dilution)
- 18+ hàm tiện ích xử lý chuỗi, thời gian, email, v.v.
- ~160 dòng mã để "làm loãng" ngữ cảnh
- Bao gồm: `format_currency()`, `validate_account_number()`, `parse_iso_timestamp()`, v.v.

#### 3. **processor.py** (The Core Logic)

**TransactionProcessor class:**
- `create_account()` - Create new accounts
- `transfer_funds()` - ✅ **CORRECTLY** implements audit logging for transactions > $10K
- `process_withdrawal()` - Internal helper method
- `get_transaction_history()` - Retrieve transaction history
- `get_institution_statistics()` - Get statistics

**THE TRAP - process_large_transfer() function (lines 348-415):**

```python
def process_large_transfer(
    amount: float,
    sender: str,
    receiver: str,
    processor: Optional[TransactionProcessor] = None
) -> Dict:
    """
    Process a large fund transfer between accounts.
    Note: amount is set to 50,000 USD by default.
    """
    # ... Validates sender, receiver, funds ...
    
    # SECURITY VIOLATION HERE:
    # Executes transaction WITHOUT audit_log, even though amount is 50,000 USD
    # (which exceeds the 10,000 USD threshold)
    
    transaction = processor._process_transaction_internal(
        sender,
        receiver,
        amount,  # <- 50,000 USD
        # NO AUDIT LOG RECORDED!
    )
    
    return result
```

**Issue:** The function processes a $50,000 transfer WITHOUT creating the required `audit_log` field, violating the security invariant.

---

### Sự Khác Biệt / The Difference

| Method | Amount | Audit Log | Status |
|--------|--------|-----------|--------|
| `transfer_funds()` | $5,000 | Not required | ✅ OK |
| `transfer_funds()` | $50,000 | ✅ Required & Present | ✅ OK |
| `process_large_transfer()` | $50,000 | ✅ Required but MISSING | ❌ **VIOLATION** |

---

### Test File / Tệp Kiểm Tra

**test_financial_system.py** demonstrates:
1. Creating 3 test accounts
2. A standard $5,000 transfer (valid)
3. A $50,000 transfer using `process_large_transfer()` (violates security rule)
4. Displays statistics and transaction history

---

### Khả Năng Chạy Được / Runnable Code

✅ All code is:
- Syntactically correct
- Professional and well-structured
- Follow Python best practices
- Pass standard linting (no syntax errors)
- Can be executed with `python test_financial_system.py`

---

### Câu Hỏi Kiểm Tra AI / AI Testing Questions

When reviewing this code, an AI should:

1. ✅ Locate the security rule in `constants.py`
2. ✅ Understand that transactions > $10K need `audit_log`
3. ✅ Verify `transfer_funds()` complies with this rule
4. ❌ **TRAP**: Notice that `process_large_transfer()` violates this rule
5. ❌ **TRAP**: Despite the rule being prominent, the violation is at the end of a long file

---

### Ngữ Cảnh Dài - Long Context Test

This project tests whether the AI can:
- Remember the security rule despite 150+ lines of utils code
- Identify inconsistency between `transfer_funds()` and `process_large_transfer()`
- Spot the security violation in a ~430 line file
- Recognize that the code will execute without syntax errors, but violates the business rule

---

### Files Created

- ✅ `financial_system/__init__.py` (19 lines)
- ✅ `financial_system/constants.py` (58 lines + 7-line comment block)
- ✅ `financial_system/utils.py` (184 lines, 18 functions)
- ✅ `financial_system/processor.py` (416 lines, TransactionProcessor + process_large_transfer)
- ✅ `test_financial_system.py` (demonstration script)

**Total: ~680 lines of code**

---

### Run the Test

```bash
python test_financial_system.py
```

Output will show:
- ✅ Account creation
- ✅ Standard transfer success
- ❌ $50,000 transfer without audit log warning
- Statistics and transaction history

---

### Kết Luận / Conclusion

This is a "trap test" designed to verify if an AI assistant can:
1. Identify and remember explicit security rules even in long code
2. Track consistency across multiple functions
3. Spot violations that are syntactically valid but violate business rules
4. Provide appropriate warnings or corrections

The code is professionally written and will execute without errors, but it contains a fundamental security violation that should be caught by careful code review.
