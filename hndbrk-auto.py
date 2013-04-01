import os
import subprocess
import sys
import user
import io
import commands
import time
import argparse
#/Applications/HandBrakeCLI -i /Volumes/ENTERPRISE_S3D1_UK/

env_handbrake_home = os.getenv('HANDBRAKE_HOME', '__NO_HANDBRAKE_HOME_SET__')
env_handbrake_cli = os.getenv('HANDBRAKE_CLI', env_handbrake_home + '/HandbrakeCLI')

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="The input source")
parser.add_argument("-o", "--output-dir", help="The output directory for the files")
parser.add_argument("-Z", "--preset", help="Which preset to use", default="Normal")
parser.add_argument("-m", "--minimum-minutes", help="Minimum number of minutes for each episode", type=int, default=600)
parser.add_argument("-x", "--executable", help="Path to executable", default=env_handbrake_cli)
args = parser.parse_args()

print args

if not os.access(args.executable, os.X_OK):
    print("Must provide system environment variable HANDBRAKE_HOME to specify home directory of HandbrakeCLI binary,"
          " or HANDBRAKE_CLI to specify full path to binary")
    sys.exit(-1)

find_cmd = "%(executable)s -Z %(preset)s -i %(input)s --min-duration %(minimum_minutes)d -t 0"%(vars(args))
print "Executing " + find_cmd
find_status, find_out = commands.getstatusoutput(find_cmd)
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


