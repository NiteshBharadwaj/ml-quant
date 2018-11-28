import QuantLib as ql
import math
from vol_models.data_utils import get_ir_ts, get_implied_vols_sticky_strike


class VolModel:
    def __init__(self, vol_data):
        self.vol_data = vol_data
        self.init_defaults()
    def get_vol(self, strike, time):
        pass
    def get_variance(self, strike, time):
        vol = self.get_vol(strike, time)
        return vol*vol*time
    def init_defaults(self):
        self.day_count = ql.Actual365Fixed()
        self.calendar = ql.UnitedStates()
        self.calculation_date = ql.Date(self.vol_data.market_date.day, self.vol_data.market_date.month, self.vol_data.market_date.year)
        self.spot = self.vol_data.spot
        # This is a dangerous hook. TODO: make the evaluation date dynamic
        # Danger is avoided now by having same market date across data
        ql.Settings.instance().evaluationDate = self.calculation_date
        self.dom_ts = get_ir_ts(self.vol_data.smiles, True, self.calculation_date, self.day_count)
        self.for_ts = get_ir_ts(self.vol_data.smiles, False, self.calculation_date, self.day_count)
        self.strikes = self.vol_data.strikes
        self.expiration_dates, implied_vols = \
            get_implied_vols_sticky_strike(self.vol_data.smiles)
        self.implied_vols = ql.Matrix(len(self.strikes), len(self.expiration_dates))
        for i in range(self.implied_vols.rows()):
            for j in range(self.implied_vols.columns()):
                self.implied_vols[i][j] = implied_vols[j][i]
