#!/usr/bin/env python

import glob
import os

from genutil import StringConstructor

from pcmdi_metrics.driver.pmp_parser import PMPParser
from pcmdi_metrics.precip_variability.lib import (
    AddParserArgument,
    precip_variability_across_timescale,
)

# Read parameters
P = PMPParser()
P = AddParserArgument(P)
param = P.get_parameter()
mip = param.mip
mod = param.mod
var = param.var
dfrq = param.frq
modpath = param.modpath
prd = param.prd
fac = param.fac
nperseg = param.nperseg
noverlap = param.noverlap
print(modpath)
print(mod)
print(prd)
print(nperseg, noverlap)

# Get flag for CMEC output
cmec = param.cmec

# Create output directory
case_id = param.case_id
outdir_template = param.process_templated_argument("results_dir")
outdir = StringConstructor(
    str(outdir_template(output_type="%(output_type)", mip=mip, case_id=case_id))
)
for output_type in ["graphics", "diagnostic_results", "metrics_results"]:
    if not os.path.exists(outdir(output_type=output_type)):
        try:
            os.makedirs(outdir(output_type=output_type))
        except FileExistsError:
            pass
    print(outdir(output_type=output_type))

# Check data in advance
file_list = sorted(glob.glob(os.path.join(modpath, "*" + mod + "*")))
data = []
for file in file_list:
    if mip == "obs":
        model = file.split("/")[-1].split(".")[2]
        data.append(model)
    else:
        model = file.split("/")[-1].split(".")[2]
        ens = file.split("/")[-1].split(".")[3]
        data.append(model + "." + ens)

print("Number of datasets:", len(file_list))
print("Dataset:", data)

# Regridding -> Anomaly -> Power spectra -> Domain&Frequency average -> Write
syr = prd[0]
eyr = prd[1]

for dat, file in zip(data, file_list):
    """
    1. Spatial Distribution of Mean State
    1-1 Mean climate 
    1-2 Mean climate 

    2. Seasonal Cycle
    2-1 Amplitude + Phase of Seasonal Cycle
    2-2 Monthly score (RMS error)
    """
    mean_climate_pr(file, syr, eyr, mip, dat, var, XXXX)

    # Precipitation variability across time scales
    precip_variability_across_timescale(
        file, syr, eyr, dfrq, mip, dat, var, fac, nperseg, noverlap, outdir, cmec
    )

    # Diunal Cycle
    precip_diunal_cycle(file, syr, eyr, mip, dat, var, XXXX)