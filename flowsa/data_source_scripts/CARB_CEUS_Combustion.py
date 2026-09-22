# CARB_CEUS_Combustion.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8

"""
Static attribution weights for splitting CARB's "Commercial, Not Specified"
coal/petroleum/wood fuel-combustion residual (NAICS 531 in the original
StateGHGI_CA crosswalk) across the actual commercial tenant NAICS that use
that fuel. Weights are natural-gas + other-fuel usage (MTherm) by CEC CEUS
2022 building activity (Appendix K, Table 6-1, sheet 'Statewide'), spread
across each activity's constituent NAICS by CA economic output share, then
to NAICS6 (equal split within a BEA_Detail's constituent NAICS6 codes).

Built by scripts/build_fix3c_rmp_weights.py's sibling logic in the CA
building-materials EEIO detail pipeline (build_ceus_weights() in
step3_final.py) - see that function's docstring for the full CEUS
methodology. Regenerate CARB_CEUS_Combustion_Weights_Raw.csv from that
pipeline if CEUS, the concordance, or CA output data are updated.
"""

import pandas as pd
from flowsa.location import US_FIPS
from flowsa.settings import externaldatapath
from flowsa.flowbyfunctions import assign_fips_location_system

CA_FIPS = '06000'


def carb_ceus_combustion_parse(*, year, **_):
    df = pd.read_csv(externaldatapath / "CARB_CEUS_Combustion_Weights_Raw.csv")
    df = df.rename(columns={"NAICS6": "ActivityProducedBy",
                             "weight": "FlowAmount"})
    df["Class"] = "Other"
    df["SourceName"] = "CARB_CEUS_Combustion"
    df["FlowName"] = "Combustion weight"
    df["FlowType"] = "TECHNOSPHERE_FLOW"
    df["Compartment"] = None
    df["Unit"] = "share"
    df["Location"] = CA_FIPS
    df["Year"] = year
    df = assign_fips_location_system(df, '2015')
    df["DataReliability"] = 4
    df["DataCollection"] = 4
    return df
