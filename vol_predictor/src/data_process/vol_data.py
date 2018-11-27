class VolSmileData:
    def __init__(self, pillar_date, rd, rf, vols):
        self.pillar_date = pillar_date
        self.rd = rd
        self.rf = rf
        self.vols = vols
# Sticky Strike
class VolSurfaceData:
    def __init__(self, underlying_name, market_date, spot_date, spot, strikes, smiles):
        self.underlying_name = underlying_name
        self.market_date = market_date
        self.spot_date = spot_date
        self.spot = spot
        self.strikes = strikes
        self.smiles = smiles
