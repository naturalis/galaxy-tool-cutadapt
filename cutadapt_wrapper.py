"""
Marten Hoogeveen    V1.0
Dick Groenenberg    V1.1

This script is made for the Naturalis galaxy instance and is a wrapper for the tool cutadapt.(https://github.com/marcelm/cutadapt)
Cutadapt finds and removes adapter sequences, primers, poly-A tails and other types of unwanted sequence from your high-throughput sequencing reads.
The wrapper is made so it can process zip files containing multiple fastq files.

"""
# according to 2to3 this script is compatible with Python3
# adjustments were required because of strict separation between strings and binary data in Python3
# due to the upgrade to cutadapt v.2.x the syntax for anchored adaptors changed (5' now preceded with ^)

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
requiredArguments.add_argument('-t', '--input_type', metavar='FASTQ, FASTA GZ input', dest='input_type', type=str,
                               help='Sets the input type, gz or FASTQ', required=True)
requiredArguments.add_argument('-fp', '--forward_primer', metavar='forward primer sequence', dest='forward_primer', type=str,
                               help='Forward primer that needs to be trimmed off, only check the beginning of the sequence', required=False, nargs='?', default="")
requiredArguments.add_argument('-rp', '--reverse_primer', metavar='reverse primer sequence', dest='reverse_primer', type=str,
                               help='Reverse primer that need to be trimmed off', required=False, nargs='?', default="")
requiredArguments.add_argument('-e', '--error_rate', metavar='error rate', dest='error_rate', type=str,
                               help='Accepted error rate for primer trimming', required=True, nargs='?', default="")
requiredArguments.add_argument('-l', '--min_length', metavar='minimum read length that will be written to the output file', dest='min_length', type=str,
                               help='minimum read length that will be written to the output file', required=True, nargs='?', default="")
requiredArguments.add_argument('-O', '--overlap', metavar='Number of bases that need to overlap with the primer', dest='overlap', type=str,
                               help='Number of bases that need to overlap with the primer', required=True, nargs='?', default="")
requiredArguments.add_argument('-of', '--folder_output', metavar='folder output', dest='out_folder', type=str,
                               help='Folder name for the output files', required=True)
requiredArguments.add_argument('-ts', '--trim_strategy', metavar='trim strategy', dest='trim_strategy', type=str,
                               help='trim strategies for trimming', required=False)
requiredArguments.add_argument('-un', '--untrimmed', metavar='untrimmed', dest='untrimmed', type=str,
                               help='Output the non-trimmed sequences', required=False)
requiredArguments.add_argument('-command_line', '--command_line_prarameters', metavar='advanced input mode', dest='command_line', type=str,
                               help='Use command line parameters', required=False, nargs='?', default="")
args = parser.parse_args()

def admin_log(tempdir, out=None, error=None, function=""):
    """
    A log file will be made and log data will be written to that file. Most of the time this is the stdout and stderror
    of the shell. In the log it says if the message in is coming from stdout or stderror.
    :param tempdir: the tempdir path that contains the log file
    :param out: stdout or out message
    :param error: stderror or error message
    :param function: name of the function or step that generated the message
    """

    with open(tempdir + "/adminlog.log", 'a') as adminlogfile:
        separation = 60 * "="
        if type(out)==str:
            adminlogfile.write("out " + str(function) + " \n" + str(separation) + "\n" + str(out) + "\n\n")
        else:
            adminlogfile.write("out "+ str(function) + " \n" + str(separation) + "\n" + out.decode() + "\n\n")
        if error:
            adminlogfile.write("error " + str(function) + "\n" + str(separation) + "\n" + str(error) + "\n\n")

def make_output_folders(tempdir):
    """
    Output en work folders are created. The wrapper uses these folders to save the files that are used between steps.
    :param tempdir: tempdir path
    """
    call(["mkdir", "-p", tempdir])
    call(["mkdir", tempdir + "/files"])
    call(["mkdir", tempdir + "/output"])
    call(["mkdir", tempdir + "/output/trimmed"])
    call(["mkdir", tempdir + "/output/untrimmed"])

def gunzip(tempdir):
    """
    If the input zip file contains gzip files they need to be gunzipped. The files are gunzipped and placed in the
    files folder. The characters dash, dot and space are replaced by an underscore.
    :param tempdir: tempdir path
    """
    filetype = tempdir + "/files/*.gz"
    gzfiles = [os.path.basename(x) for x in sorted(glob.glob(filetype))]
    for x in gzfiles:
        call(["gunzip", tempdir + "/files/" + x])   #---- not the function calling itself; gunzip is a requirement for this wrapper
        gunzip_filename = os.path.splitext(x[:-3])  #---- unlike zip, gunzip removes the original .gz files!!

def changename(tempdir):
    """
    The input file need to be renamed. The characters dash, dot and space are replaced by an underscore.
    Only files with the extension fq or fastq are used.
    :param tempdir:tempdir path
    """
    fq_filetypes = [tempdir+"/files/*.fq", tempdir+"/files/*.fastq",tempdir + "/files/*.fasta", tempdir + "/files/*.fa", tempdir + "/files/*.fna"]
    files = []
    for file in fq_filetypes:
        files.extend([os.path.basename(x) for x in sorted(glob.glob(file))])
    for x in files:
        filename = os.path.splitext(x)
        fastq_filename = filename[0].translate((str.maketrans("-. ", "___"))) + filename[1]
        if x != fastq_filename:
            call(["mv", tempdir + "/files/" + x,tempdir + "/files/" + fastq_filename])


def cutadapt(tempdir):
    """
    This method loops trough all the fastq files and trims the primers per file.
    :param tempdir:tempdir path
    """
    fq_filetypes = [tempdir + "/files/*.fq", tempdir + "/files/*.fastq",tempdir + "/files/*.fasta", tempdir + "/files/*.fa", tempdir + "/files/*.fna"]
    files = []
    for file in fq_filetypes:
        files.extend([os.path.basename(x) for x in sorted(glob.glob(file))])
    for x in files:
        # removed "." in next two lines to prevent "filename..gz"
        output_name = os.path.splitext(x)[0]+"_trimmed"+str(os.path.splitext(x)[1])
        output_name_untrimmed = os.path.splitext(x)[0] + "_untrimmed"+str(os.path.splitext(x)[1])

        if args.trim_strategy == "forward_mode":
            out, error = Popen(["cutadapt", "-g", args.forward_primer, "-e", args.error_rate, "-m", args.min_length, "-O", args.overlap ,"-o", tempdir+"/output/trimmed/"+output_name, "--untrimmed-output",tempdir+"/output/untrimmed/"+output_name_untrimmed ,tempdir+"/files/"+x], stdout=PIPE, stderr=PIPE).communicate()
            admin_log(tempdir, out=out, error=error, function="cutadapt forward only")

        if args.trim_strategy == "reverse_mode":
            out, error = Popen(["cutadapt", "-a", args.reverse_primer, "-e", args.error_rate, "-m", args.min_length, "-O", args.overlap , "-o", tempdir+"/output/trimmed/"+output_name,"--untrimmed-output", tempdir+"/output/untrimmed/"+output_name_untrimmed, tempdir+"/files/"+x], stdout=PIPE, stderr=PIPE).communicate()
            admin_log(tempdir, out=out, error=error, function="cutadapt reverse only")

        if args.trim_strategy == "both_mode":
            out, error = Popen(["cutadapt", "-g", args.forward_primer+"..."+args.reverse_primer, "-e", args.error_rate, "-m", args.min_length, "-O", args.overlap , "-o", tempdir+"/output/trimmed/"+output_name,"--untrimmed-output", tempdir+"/output/untrimmed/"+output_name_untrimmed, tempdir+"/files/"+x], stdout=PIPE, stderr=PIPE).communicate()
            admin_log(tempdir, out=out, error=error, function="cutadapt both needs to be present")

        if args.trim_strategy == "both_mode_anchored":
            out, error = Popen(["cutadapt", "-a", "^"+args.forward_primer+"..."+args.reverse_primer+"$", "-e", args.error_rate, "-m", args.min_length, "-O", args.overlap , "-o", tempdir+"/output/trimmed/"+output_name,"--untrimmed-output", tempdir+"/output/untrimmed/"+output_name_untrimmed, tempdir+"/files/"+x], stdout=PIPE, stderr=PIPE).communicate()
            admin_log(tempdir, out=out, error=error, function="cutadapt both needs to be present and anchored")

        if args.trim_strategy == "both_three_optional_mode":
            out, error = Popen(["cutadapt", "-a", args.forward_primer+"..."+args.reverse_primer, "-e", args.error_rate, "-m", args.min_length, "-O", args.overlap , "-o", tempdir+"/output/trimmed/"+output_name,"--untrimmed-output", tempdir+"/output/untrimmed/"+output_name_untrimmed, tempdir+"/files/"+x], stdout=PIPE, stderr=PIPE).communicate()
            admin_log(tempdir, out=out, error=error, function="cutadapt both_three_optional_mode")
        """
        if args.trim_strategy == "advanced_mode":
            if "|" in args.command_line:
                admin_log(tempdir, error="pipe sign not allowed", function="cutadapt advanced")
            else:
                command = args.command_line.split(" ")
                base_command = ["cutadapt", "-o", tempdir + "/output/" + x]
                base_command.extend(command)
                base_command.append(tempdir + "/files/" + x)
                out, error = Popen(base_command, stdout=PIPE, stderr=PIPE).communicate()
                admin_log(tempdir, out=out, error=error, function="cutadapt advanced")
        """
        call(["rm", tempdir + "/files/"+x])

def zip_it_up(tempdir):
    out, error = Popen(["zip", "-j","-r", tempdir+"/output/trimmed.zip", tempdir+"/output/trimmed/"], stdout=PIPE,stderr=PIPE).communicate()
    admin_log(tempdir, out=out, error=error, function="zip it up")
    if args.untrimmed == "yes":
        out, error = Popen(["zip", "-j", "-r", tempdir + "/output/untrimmed.zip", tempdir + "/output/untrimmed/"], stdout=PIPE,stderr=PIPE).communicate()
        admin_log(tempdir, out=out, error=error, function="zip it up untrimmed")


def main():
    tempdir = args.out_folder
    admin_log(tempdir, out=args.trim_strategy, function="trim strategy")
    make_output_folders(tempdir)
    zip_out, zip_error = Popen(["unzip", args.inzip, "-d", tempdir.strip() + "/files"], stdout=PIPE,stderr=PIPE).communicate()
    admin_log(tempdir, zip_out, zip_error)
    if args.input_type == "gz":
        gunzip(tempdir)
    changename(tempdir)     # checking for invalid chars (-. ) is now done with changename-function for all files (after (g)unzip)
    cutadapt(tempdir)
    zip_it_up(tempdir)

if __name__ == '__main__':
    main()
