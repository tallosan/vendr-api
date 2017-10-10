#
# KProperty signals.
#
# ========================================================

from django.dispatch import Signal


openhouse_create_signal = Signal(providing_args=['resource'])
openhouse_change_signal = Signal(providing_args=['resource'])
openhouse_cancel_signal = Signal(providing_args=['resource'])
openhouse_start_signal = Signal(providing_args=['resource'])

