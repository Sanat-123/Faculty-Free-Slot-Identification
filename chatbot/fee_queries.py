"""
---------------------------------------------------------
Fee Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL FEE COLLECTION
# ==========================================================

def total_fee_collection():

    query = """
    SELECT SUM(amount)
    FROM warehouse.fees
    WHERE status='Paid';
    """

    result = execute_query(query)

    return f"💰 Total Fee Collected : ₹{result[0][0]:,.2f}"


# ==========================================================
# TOTAL PENDING FEES
# ==========================================================

def total_pending_fee():

    query = """
    SELECT SUM(amount)
    FROM warehouse.fees
    WHERE status='Pending';
    """

    result = execute_query(query)

    if result[0][0] is None:
        return "💰 Pending Fee : ₹0"

    return f"💰 Pending Fee : ₹{result[0][0]:,.2f}"


# ==========================================================
# PAID vs PENDING SUMMARY
# ==========================================================

def fee_status_summary():

    query = """
    SELECT status,
           COUNT(*),
           SUM(amount)
    FROM warehouse.fees
    GROUP BY status
    ORDER BY status;
    """

    result = execute_query(query)

    output = "\n📊 Fee Status Summary\n"
    output += "-" * 55 + "\n"

    for row in result:

        output += (
            f"{row[0]} : "
            f"{row[1]} Students | "
            f"₹{row[2]:,.2f}\n"
        )

    return output


# ==========================================================
# STUDENT FEE DETAILS
# ==========================================================

def student_fee(student_id):

    query = f"""
    SELECT
        student_id,
        amount,
        status,
        payment_date
    FROM warehouse.fees
    WHERE student_id='{student_id}';
    """

    result = execute_query(query)

    if not result:
        return "Student not found."

    output = "\n🎓 Student Fee Details\n"
    output += "-" * 55 + "\n"

    for row in result:

        output += (
            f"\nStudent ID   : {row[0]}\n"
            f"Amount       : ₹{row[1]:,.2f}\n"
            f"Status       : {row[2]}\n"
            f"Payment Date : {row[3]}\n"
        )

    return output


# ==========================================================
# RECENT PAYMENTS
# ==========================================================

def recent_payments(limit=10):

    query = f"""
    SELECT
        student_id,
        amount,
        payment_date
    FROM warehouse.fees
    WHERE status='Paid'
    ORDER BY payment_date DESC
    LIMIT {limit};
    """

    result = execute_query(query)

    output = "\n🧾 Recent Payments\n"
    output += "-" * 60 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"₹{row[1]:,.2f} | "
            f"{row[2]}\n"
        )

    return output


# ==========================================================
# TEST MODULE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FEE QUERY MODULE")
    print("=" * 60)

    print("\nTotal Fee Collection")
    print(total_fee_collection())

    print("\nPending Fee")
    print(total_pending_fee())

    print("\nFee Status Summary")
    print(fee_status_summary())

    print("\nStudent Fee")
    print(student_fee("S0001"))

    print("\nRecent Payments")
    print(recent_payments())