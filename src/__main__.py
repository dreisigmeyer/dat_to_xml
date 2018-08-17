import glob
from multiprocessing import Process
from src.dat_to_xml import convert_to_xml
import sys


def split_seq(seq, num_processes):
    """
    Slices a list into number_of_processes pieces
    of roughly the same size
    """
    num_files = len(seq)
    if num_files < num_processes:
        num_processes = num_files
    size = num_processes
    newseq = []
    splitsize = 1.0 / size * num_files
    for i in range(size):
        newseq.append(
            seq[int(round(i * splitsize)):int(round((i + 1) * splitsize))])
    return newseq


number_of_processes = int(sys.argv[1])
dat_path = 'dat_files/'
dat_files = glob.glob(dat_path + '*')
directories_list = split_seq(dat_files, number_of_processes)
procs = []
for chunk in directories_list:
    p = Process(target=convert_to_xml, args=(chunk,))
    procs.append(p)
    p.start()
