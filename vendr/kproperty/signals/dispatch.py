#
# KProperty signals.
#
# ========================================================

from django.dispatch import Signal


openhouse_start_signal = Signal(providing_args=['resource'])

