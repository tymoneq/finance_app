
def calculate_total_loan_amount(user):
    total_amount = sum(loan.amount for loan in user.loans.all())
    return total_amount

