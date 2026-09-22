# CARB_RMP_Refrigerant.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8

"""
Static attribution weights for splitting CARB's "Commercial, Not Specified"
use-of-substitutes-for-ODS (HFC refrigerant leakage) residual (NAICS 531 in
the original StateGHGI_CA crosswalk) across the actual commercial tenant
NAICS that operate that refrigeration/AC equipment. Weights are built from
CARB's own 2009 Refrigerant Management Program rulemaking (ISOR Appendix B,
Tables 4/5/9/10: facility count x charge size x leak rate x refrigerant GWP
mix by equipment category, mapped to NAICS) - the same analysis CARB used to
justify the RMP rule, not an external proxy.

Built by scripts/build_fix3c_rmp_weights.py in the CA building-materials
EEIO detail pipeline. Regenerate CARB_RMP_Refrigerant_Weights_Raw.csv from
that script if the ISOR tables or the concordance are updated.
"""

import pandas as pd
from flowsa.settings import externaldatapath
from flowsa.flowbyfunctions import assign_fips_location_system

CA_FIPS = '06000'


def carb_rmp_refrigerant_parse(*, year, **_):
    df = pd.read_csv(externaldatapath / "CARB_RMP_Refrigerant_Weights_Raw.csv")
    df = df.rename(columns={"NAICS6": "ActivityProducedBy",
                             "weight": "FlowAmount"})
    df["Class"] = "Other"
    df["SourceName"] = "CARB_RMP_Refrigerant"
    df["FlowName"] = "Refrigerant weight"
    df["FlowType"] = "TECHNOSPHERE_FLOW"
    df["Compartment"] = None
    df["Unit"] = "share"
    df["Location"] = CA_FIPS
    df["Year"] = year
    df = assign_fips_location_system(df, '2015')
    df["DataReliability"] = 4
    df["DataCollection"] = 4
    return df
