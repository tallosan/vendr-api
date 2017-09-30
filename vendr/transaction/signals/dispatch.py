#
# KProperty signals.
#
# =============================================================


from django.dispatch import Signal

# Transaction signals.
transaction_withdraw_signal = Signal(providing_args=['request_sender'])

# Offer signals.
offer_withdraw_signal = Signal(providing_args=[])

# Contract signals.
contract_withdraw_signal = Signal(providing_args=[])

# Clause signals.
clause_change_signal = Signal(providing_args=[])

# Stage advancement signals.
advance_stage_signal = Signal(providing_args=['request_sender'])

