#!/usr/bin/python
"""
Marten Hoogeveen    marten.hoogeveen@naturalis.nl V1.0

This script is made for the Naturalis galaxy instance and is a wrapper for the tool cutadapt.(https://github.com/marcelm/cutadapt)
Cutadapt finds and removes adapter sequences, primers, poly-A tails and other types of unwanted sequence from your high-throughput sequencing reads.
The wrapper is made so it can process zip files containing multiple fastq files
"""
import sys, os, argparse
import glob
import string
from Bio import SeqIO
from subprocess import call, Popen, PIPE

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='')
requiredArguments = parser.add_argument_group('required arguments')

requiredArguments.add_argument('-i', '--input', metavar='input zipfile', dest='inzip', type=str,
                               help='Inputfile in zip format', required=True)
requiredArguments.add_argument('-t', '--input_type', metavar='FASTQ or GZ input', dest='input_type', type=str,
                               help='Sets the input type, gz or FASTQ', required=True)
requiredArguments.add_argument('-advanced', '--advanced_mode', metavar='advanced input mode', dest='advanced', type=str,
                               help='Use command line parameters', required=True, nargs='?', default="")
requiredArguments.add_argument('-command_line', '--command_line_prarameters', metavar='advanced input mode', dest='command_line', type=str,
                               help='Use command line parameters', required=True, nargs='?', default="")
requiredArguments.add_argument('-e', '--error_rate', metavar='error rate', dest='error_rate', type=str,
                               help='Accepted error rate for primer trimming', required=True, nargs='?', default="")
requiredArguments.add_argument('-fp', '--forward_primer', metavar='forward primer sequence', dest='forward_primer', type=str,
                               help='Forward primer that needs to be trimmed off, only check the beginning of the sequence', required=True, nargs='?', default="")
requiredArguments.add_argument('-rp', '--reverse_primer', metavar='reverse primer sequence', dest='reverse_primer', type=str,
                               help='Reverse primer that need to be trimmed off', required=True, nargs='?', default="")
requiredArguments.add_argument('-l', '--min_length', metavar='minimum read length that will be written to the output file', dest='min_length', type=str,
                               help='minimum read length that will be written to the output file', required=True, nargs='?', default="")
requiredArguments.add_argument('-o', '--output', metavar='output', dest='out', type=str,
                               help='Output in zip format', required=True, nargs='?', default="")
requiredArguments.add_argument('-ol', '--output_log', metavar='output_log', dest='out_log', type=str,
                               help='output log file', required=True, nargs='?', default="")
#output folder
requiredArguments.add_argument('-of', '--folder_output', metavar='folder output', dest='out_folder', type=str,
                               help='Folder name for the output files', required=True)

args = parser.parse_args()

def admin_log(tempdir, out=None, error=None, function=""):
    with open(tempdir + "/adminlog.log", 'a') as adminlogfile:
        seperation = 60 * "="
        if out:
            adminlogfile.write("out "+ function + " \n" + seperation + "\n" + out + "\n\n")
        if error:
            adminlogfile.write("error " + function + "\n" + seperation + "\n" + error + "\n\n")

def make_output_folders(tempdir):
    call(["mkdir", "-p", tempdir])
    call(["mkdir", tempdir + "/files"])
    call(["mkdir", tempdir + "/output"])

def gunzip(tempdir):
    filetype = tempdir + "/files/*.gz"
    gzfiles = [os.path.basename(x) for x in sorted(glob.glob(filetype))]
    for x in gzfiles:
        call(["gunzip", tempdir + "/files/" + x])
        gunzip_filename = os.path.splitext(x[:-3])
        call(["mv", tempdir + "/files/" + x[:-3], tempdir + "/files/" +gunzip_filename[0].translate((string.maketrans("-. " , "___")))+gunzip_filename[1]])

def changename(tempdir):
    fq_filetypes = [tempdir+"/files/*.fq", tempdir+"/files/*.fastq"]
    files = []
    for file in fq_filetypes:
        files.extend([os.path.basename(x) for x in sorted(glob.glob(file))])
    for x in files:
        filename = os.path.splitext(x)
        fastq_filename = filename[0].translate((string.maketrans("-. ", "___"))) + filename[1]
        if x != fastq_filename:
            call(["mv", tempdir + "/files/" + x,tempdir + "/files/" + fastq_filename])


def cutadapt(tempdir):
    fq_filetypes = [tempdir + "/files/*.fq", tempdir + "/files/*.fastq"]
    files = []
    for file in fq_filetypes:
        files.extend([os.path.basename(x) for x in sorted(glob.glob(file))])
    for x in files:
        output_name = os.path.splitext(x)[0]+"_trimmed.fastq"
        if args.advanced:
            if "|" in command:
                admin_log(tempdir, error="pipe sign not allowed", function="cutadapt")
            else:
                command = args.command_line.split(" ")
                base_command = ["cutadapt", "-o", tempdir + "/output/" + x]
                base_command.extend(command)
                base_command.append(tempdir + "/files/" + x)
                out, error = Popen(base_command, stdout=PIPE,stderr=PIPE).communicate()
        else:
            out, error = Popen(["cutadapt","-a",args.forward_primer+"..."+args.reverse_primer,"-e", args.error_rate ,"--trimmed-only", "-m", args.min_length , "-o", tempdir+"/output/"+output_name, tempdir+"/files/"+x], stdout=PIPE, stderr=PIPE).communicate()
        admin_log(tempdir, out=out, error=error, function="cutadapt")
        call(["rm", tempdir + "/files/"+x])

def zip_it_up(tempdir):
    call(["zip","-r","-j", tempdir+"/trimmed.zip", tempdir+"/output/"],stdout=open(os.devnull, 'wb'))
    #call(["mv", tempdir + ".zip", args.out])#

def main():
    #tempdir = Popen(["mktemp", "-d", "XXXXXX"], stdout=PIPE, stderr=PIPE).communicate()[0].strip()
    tempdir = args.out_folder
    make_output_folders(tempdir)
    zip_out, zip_error = Popen(["unzip", args.inzip, "-d", tempdir.strip() + "/files"], stdout=PIPE,stderr=PIPE).communicate()
    admin_log(tempdir, zip_out, zip_error)
    if args.input_type == "gz":
        gunzip(tempdir)
    else:
        changename(tempdir)
        cutadapt(tempdir)
    zip_it_up(tempdir)
    #call(["mv", tempdir + "/adminlog.log", args.out_log])
    #call(["rm", "-rf", tempdir])

if __name__ == '__main__':
    main()



