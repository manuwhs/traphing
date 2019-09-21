class MarketHours():
    """
    This class is meant to handle all the information and processing related to
    the opening market hours of a given asset
    """
    def __init__(self):
        self.open_time = None
        self.close_time = None
        
    def estimate_openMarketTime(self):
        # If we do not know the period in which the market should be open, this function
        # will try to guess it from the data. There is some weird assets like the Forex
        # that are only open one hour on Sundays. Also, the timeZone can create problems.
        
        openTimes = []
        closeTimes = [] 
        
        dates = self.get_dates()
        days, indexDaysDict = self.get_indexDictByDay()
    #    print days
        for day in days:
            openTimeindex = indexDaysDict[day][0]
    #        print openTimeindex
            openTimes.append(dates[openTimeindex].time())
            closeTimes.append(dates[indexDaysDict[day][-1]].time())
            
        openTime = min(openTimes)
        closeTime = max(closeTimes)
        
        return [openTime, closeTime]

    def estimate_timeframe(self):
        # If we do not know the period of the signal a priori, we will try to guess it
        # This function is automatically called if the period is None and need to be used.
        dates = self.get_dates()
    #    dates = ul.convert2dt(dates)
    #    diffs = dates[1:] - dates[:-1]
    #             # bMA.diff(dates)
        diffs = ul.diff_dates(dates)
    #    print diffs
        min_pediod_min = min(diffs).total_seconds() / 60
        return min_pediod_min
    