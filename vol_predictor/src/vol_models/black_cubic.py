from .base_model import VolModel
import QuantLib as ql


class BlackCubic(VolModel):
    def __init__(self, vol_data):
        super().__init__(vol_data)
        self.surface = ql.BlackVarianceSurface(self.calculation_date, self.calendar,
                                               self.expiration_dates, self.strikes,
                                               self.implied_vols, self.day_count)

    def get_vol(self, strike, time, recalibrate=True):
        return self.surface.blackVol(time, strike)
