from .base_model import VolModel
import QuantLib as ql


class DupireLocal(VolModel):
    def __init__(self, vol_data):
        super().__init__(vol_data)

        self.bl_surface = ql.BlackVarianceSurface(self.calculation_date, self.calendar,
                                                  self.expiration_dates, self.strikes,
                                                  self.implied_vols, self.day_count)
        self.surface = ql.LocalVolSurface(ql.BlackVolTermStructureHandle(self.bl_surface),
                                          self.dom_ts, self.for_ts, self.spot)

    def get_vol(self, strike, time, recalibrate=True):
        return self.surface.localVol(time, strike)
