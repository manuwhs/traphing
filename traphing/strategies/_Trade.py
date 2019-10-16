
class Trade:
    """
    Information class about a trade
    """
    def __init__(self, trade_id, entry_signal,
                 trade_price, trade_timestamp):
        self.trade_id = trade_id
        self.entry_signal  = entry_signal  # Symbol of the Security (GLD, AAPL, IDX...)
        
        self.trade_price = trade_price
        self.trade_timestamp =  trade_timestamp
        
        self._copy_info_from_entry_signal()
        
    def _copy_info_from_entry_signal(self):
        self.BUYSELL = self.entry_signal.BUYSELL
        self.strategy_id = self.entry_signal.strategy_id
        self.entry_signal_id = self.entry_signal.entry_signal_id
        