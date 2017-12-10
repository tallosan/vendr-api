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
contract_create_signal = Signal(providing_args=[])
contract_withdraw_signal = Signal(providing_args=['resource'])

# Clause signals.
clause_change_signal = Signal(providing_args=['n_changes', 'resource'])

# Closing stage signals.
amendment_created_signal = Signal(providing_args=[])
amendment_accepted_signal = Signal(providing_args=[])

waiver_created_signal = Signal(providing_args=[])
waiver_accepted_signal = Signal(providing_args=[])

nof_accepted_signal = Signal(providing_args=[])

# Stage advancement signals.
advance_stage_signal = Signal(providing_args=['request_sender'])

