#
# KProperty signals.
#
# =============================================================


from django.dispatch import Signal

# Offer signals.
offer_withdraw_signal = Signal(providing_args=[])

# Clause signals.
clause_change_signal = Signal(providing_args=[])

