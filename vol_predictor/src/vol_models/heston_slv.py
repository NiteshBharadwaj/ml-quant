from .base_model import VolModel
import QuantLib as ql
from QuantLib import *


class HestonSLV(VolModel):
    def __init__(self, vol_data):
        super().__init__(vol_data)
        self.process = ql.HestonProcess(self.dom_ts, self.for_ts,
                                   ql.QuoteHandle(ql.SimpleQuote(self.spot)),
                                   self.v0, self.kappa, self.theta, self.sigma, self.rho)
        self.model = ql.HestonModel(self.process)
        self.engine = ql.AnalyticHestonEngine(self.model)
        self.bl_surface = ql.BlackVarianceSurface(self.calculation_date, self.calendar,
                                           self.expiration_dates, self.strikes,
                                           self.implied_vols, self.day_count)

        self.bl_surface.setInterpolation("bicubic")
        vol_ts = ql.BlackVolTermStructureHandle(self.bl_surface)
        self.bs_process = BlackScholesMertonProcess(ql.QuoteHandle(ql.SimpleQuote(self.spot)), self.for_ts, self.dom_ts, vol_ts)


    def get_vol(self, strike, time, recalibrate=True):
        if time < 3/365.0:
            # qlib is considering these options as expired
            return self.bl_surface.blackVol(time,strike)

        # Calibrate using interpolated vols at liquid strikes
        # This may not be the standard, but we don't know the standard used by a closed system.
        # If NN is able to figure out a way to match this particular calibration, it should hopefully figure out a way to match other similar calibrations
        if recalibrate:
            self.calibrate_heston(strike, time)
        # Imply black vol from heston price
        exercise = EuropeanExercise(self.calculation_date+int(time*365.0))
        payoff = PlainVanillaPayoff(Option.Put, strike)
        option = EuropeanOption(payoff, exercise)
        option.setPricingEngine(self.engine)
        h_price = option.NPV()
        vol = option.impliedVolatility(h_price, self.bs_process)
        return vol
    def init_defaults(self):
        super().init_defaults()
        # Heston initial parameters
        self.v0 = 0.01 # Vol of vol
        self.theta = 0.02 # Mean reversion parameter
        self.rho = -0.75 # correlation
        self.sigma = 0.5 # vol
        self.kappa = 0.2 # drift factor


    def calibrate_heston(self, strike, time):
        ref_options = []
        for j, s in enumerate(self.strikes):
            p = ql.Period(int(time*365.0), ql.Days)
            sigma = self.bl_surface.blackVol(time,s)
            helper = ql.HestonModelHelper(p, self.calendar, self.spot, s,
                                          ql.QuoteHandle(ql.SimpleQuote(sigma)),
                                          self.dom_ts,
                                          self.for_ts)
            helper.setPricingEngine(self.engine)
            ref_options.append(helper)
        lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
        self.model.calibrate(ref_options, lm,
                             ql.EndCriteria(500, 50, 1.0e-8, 1.0e-8, 1.0e-8))
        self.theta, self.kappa, self.sigma, self.rho, self.v0 = self.model.params()
