import glob
from src.dat_to_xml import convert_to_xml


dat_path = 'dat_files/'
dat_files = glob.glob(dat_path + '*')
convert_to_xml(dat_files)
