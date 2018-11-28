import QuantLib as ql
import numpy as np



def get_implied_vols_sticky_strike(smiles):
    implied_vols = []
    dates = []
    for smile in smiles:
        implied_vols_for_pillar = []
        pillar_date = smile.pillar_date
        dates.append(ql.Date(pillar_date.day, pillar_date.month, pillar_date.year))
        for vol in smile.vols:
            implied_vols_for_pillar.append(vol)
        implied_vols.append(implied_vols_for_pillar)
    return dates, implied_vols


def get_ir_ts(smiles, is_dom, calculation_date, day_count):
    dates = []
    zero_rates = []
    for smile in smiles:
        pillar_date = smile.pillar_date
        dates.append(ql.Date(pillar_date.day, pillar_date.month, pillar_date.year))
        zero_rate = smile.rd if is_dom else smile.rf
        zero_rates.append(zero_rate)
    # zero_curve = ql.ZeroCurve(dates, zero_rates, ql.Actual365Fixed())
    zero_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, zero_rates[0], day_count))
    return zero_curve


def get_exp_date(smiles):
    dates = []
    for smile in smiles:
        pillar_date = smile.pillar_date
        dates.append(ql.Date(pillar_date.day, pillar_date.month, pillar_date.year))
    return dates
