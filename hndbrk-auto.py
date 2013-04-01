import os
import subprocess
import sys
import user
import io
import commands
import time
import argparse
#/Applications/HandBrakeCLI -i /Volumes/ENTERPRISE_S3D1_UK/

handbrake_home = os.getenv('HANDBRAKE_HOME', '__NO_HANDBRAKE_HOME_SET__')
handbrake_cli = os.getenv('HANDBRAKE_CLI', handbrake_home + '/HandbrakeCLI')

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="The input source")
parser.add_argument("-o", "--output-dir", help="The output directory for the files")
parser.add_argument("-x", "--executable", help="Path to executable", default=handbrake_cli)
args = parser.parse_args()

print args

handbrake_cli=args.executable
input_src = args.input

if not os.access(handbrake_cli, os.X_OK):
    print("Must provide system environment variable HANDBRAKE_HOME to specify home directory of HandbrakeCLI binary,"
          " or HANDBRAKE_CLI to specify full path to binary")
    sys.exit(-1)

find_process_args = [handbrake_cli, " -Z Normal -i /Volumes/ENTERPRISE_S3D1_UK/ -o handbrake_out.m4v --min-duration 1200 -t 0"]
print "Executing " + find_process_args.__str__()
find_status, find_out = commands.getstatusoutput(handbrake_cli + " -Z Normal -i /Volumes/ENTERPRISE_S3D1_UK/ -o handbrake_out.m4v --min-duration 1200 -t 0")
if find_status != 0:
    print("Attempting to find titles failed:")
    print(find_out)
    print("Exit")
    sys.exit(-1)

print "stuff"
print "status: " + str(find_status)
print "out: " + find_out
print "done"

#stdout_readlines = find_out.split('\\n')


