#
# Custom Decorators.
#
# ============================================================================


""" An augmented version of the @receiver decorator that can attach multiple
    signals to multiple senders. Really useful for attaching models belonging to
    any sized inheritance scheme.
    Args:
        signals (List of Signals) -- The signals that we want to connect.
        senders (List of connectables) -- A list of entities (models, functions,
	    etc.) that we want to connect to.
"""
def receiver_extended(signals, senders, **kwargs):

    """ Attach the signals to each sender.
        Args:
            func (function) -- The function handler (the function using the decorator).
    """
    def _decorator(func):
        for signal in signals:
            for sender in senders:
                signal.connect(receiver=func, sender=sender, **kwargs)
        
        return func

    return _decorator

