#!/usr/bin/env python
from pcmdi_metrics.pcmdi.pmp_parser import *
import cdms2
import cdutil
import cdtime

###
# INPUT PARAMETERS OFTEN STORED IN SEPRATE FILE

parser = PMPParser() # Includes all default options

parser.add_argument(
    '-n', '--newarg',
    dest='newarg',
    help='description',
    required=False)

parser.add_argument(
    '--model',
#   type=ast.literal_eval, #loading in a list 
    dest='model',
    help='description',
    required=False)

parser.add_argument(
    '--filename_template',
    dest='filename_template',
    help='description',
    required=False)

parser.add_argument(
    '--output_filename_template',
    dest='output_filename_template',
    help='description',
    required=False)
'''
parser.add_argument(
    '--results_dir',
    type=ast.literal_eval, #loading in a dictionary
    dest='results_dir',
    help='description',
    required=False)
parser.add_argument(
    '--mp', '--modpath',
    dest='modpath',
    help='description',
    required=False)
'''

parser.use('--results_dir')
parser.use('--modpath')

parser.add_argument(
    '--start', 
    dest='start',
    help='description',
    required=False)

parser.add_argument(
    '--end', 
    dest='end',
    help='description',
    required=False)

parser.add_argument(
    '--variable',
#   type=ast.literal_eval, #loading in a dictionary
    dest='variable',
    help='description',
    required=False)

parameter = parser.get_parameter()

models = parameter.model
modpath = parameter.modpath
filename_template = parameter.filename_template
start = parameter.start
end = parameter.end
variables = parameter.variable
results_dir = parameter.results_dir
output_filename_template = parameter.output_filename_template

start_mo = int(start.split('-')[1])
start_yr = int(start.split('-')[0])
end_mo = int(end.split('-')[1])
end_yr = int(end.split('-')[0])

# COMPUTE AND SAVE ANNUAL CYCLE CLIMATOLOGY
for mod in models:
 for var in variables:
  pathin = modpath + filename_template  
  pathin = pathin.replace('VARIABLE',var)
  pathin = pathin.replace('MODEL',mod)
  print(pathin)

  f = cdms2.open(pathin)
  d = f(var,time = (cdtime.comptime(start_yr,start_mo),cdtime.comptime(end_yr,end_mo)))
  print(d.shape)

  d_ac = cdutil.ANNUALCYCLE.climatology(d)
  d_ac.id = var
  print(d_ac.shape)

  pathout = results_dir+output_filename_template 
  pathout = pathout.replace('VARIABLE',var)
  pathout = pathout.replace('MODEL',mod)
  g = cdms2.open(pathout,'w+')
  g.write(d_ac)
  g.close()






 
