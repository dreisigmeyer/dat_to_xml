import glob
from multiprocessing import Process
import os
from shared_python_code.utility_functons import split_seq
from src.dat_to_xml import convert_to_xml
import sys

THIS_DIR = os.path.dirname(__file__)

number_of_processes = int(sys.argv[1])
dat_path = THIS_DIR + '../dat_files/'
dat_files = glob.glob(dat_path + '*')
directories_list = split_seq(dat_files, number_of_processes)
procs = []
for chunk in directories_list:
    p = Process(target=convert_to_xml, args=(chunk,))
    procs.append(p)
    p.start()
