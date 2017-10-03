#
# KProperty signals.
#
# =============================================================


from django.dispatch import Signal

# Transaction signals.
transaction_withdraw_signal = Signal(providing_args=['request_sender'])

# Offer signals.
offer_withdraw_signal = Signal(providing_args=['resource'])

# Contract signals.
contract_withdraw_signal = Signal(providing_args=['resource'])

# Clause signals.
clause_change_signal = Signal(providing_args=['n_changes', 'resource'])

# Stage advancement signals.
advance_stage_signal = Signal(providing_args=['request_sender'])

