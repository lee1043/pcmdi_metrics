import datetime

# P Gleckler, PCMDI
# Sample input paramter file for basicClim.py prototype applied to PCMDI's CMIP archive
# 20191211

ver = datetime.datetime.now().strftime('v%Y%m%d') #PCMDI versioning

mip = 'cmip6'
exp = 'historical'  # historical or amip
latest_xmls = 'v20191126'
start = '1981-01'  # For CDMS up to but not including
end = '2006-01'

modpath = '/p/user_pub/pmp/pmp_results/pmp_v1.1.2/additional_xmls/latest/' + latest_xmls + '/' + mip + '/' + exp + '/atmos/mon/VARIABLE/'

filename_template = mip + '.' + exp + '.MODEL.mon.VARIABLE.xml'

model = ['GFDL-CM4.r1i1p1f1','GFDL-ESM4.r1i1p1f1']

variable = ['rlut','pr']

output_filename_template = 'MODEL.mon.VARIABLE.' +  start.replace('-','') + '-' + end.replace('-','') + '.AC.' + ver + '.nc'

results_dir = './simple_test/'

