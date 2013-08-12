import os
import sys
import commands
import argparse
import re

name_chunks_to_remove=['_UK']

env_handbrake_home=os.getenv('HANDBRAKE_HOME', '__NO_HANDBRAKE_HOME_SET__')
env_handbrake_cli=os.getenv('HANDBRAKE_CLI', env_handbrake_home + '/HandbrakeCLI')

parser=argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="The input source", default="/dev/disk1")
parser.add_argument("-o", "--output-dir", help="The output directory for the files", default=None)
parser.add_argument("-Z", "--preset", help="Which preset to use", default="Normal")
parser.add_argument("-m", "--minimum-seconds", help="Minimum number of seconds for each episode", type=int, default=600)
parser.add_argument("-e", "--executable", help="Path to executable", default=env_handbrake_cli)
parser.add_argument("-x", "--extra-parameters", help="Extra parameters", default="")
args=parser.parse_args()

if not os.access(args.executable, os.X_OK):
    print("Must provide system environment variable HANDBRAKE_HOME to specify home directory of HandbrakeCLI binary,"
          " or HANDBRAKE_CLI to specify full path to binary")
    sys.exit(-1)

def execute_cmd(cmd):
    print "Executing " + cmd
    cmd_status, cmd_out=commands.getstatusoutput(cmd)
    if cmd_status !=0:
        print("Failed running %s:"%cmd)
        print(cmd_out)
        print("Exit")
        sys.exit(-1)
    return cmd_out

def find_episodes():
    find_cmd="%(executable)s -i %(input)s --min-duration %(minimum_seconds)d -t 0"%(vars(args))
    return execute_cmd(find_cmd)

def get_disk_name(device_name):
    disk_name_cmd="diskutil info " + device_name
    diffutil_out=execute_cmd(disk_name_cmd)
    volume_names=[line for line in diffutil_out.splitlines() if line.strip(" ").startswith("Volume Name")]
    if len(volume_names) == 0:
        raise RuntimeError("Could not find volume name")
    volume_name=volume_names[0].split(":",1)[1].strip()
    for chunk in name_chunks_to_remove:
        volume_name=volume_name.replace(chunk,'')
    print "Found volume name: " + volume_name
    return volume_name

def extract_episode(disk_name, titleNumber):
    output_file=args.output_dir + "/" + disk_name + "E" + titleNumber + ".m4v"
    if os.access(output_file, os.R_OK):
        return "File %s already exists - skipping"%output_file
    extract_cmd="%s -i %s -o %s -t %s --preset %s %(extra_parameters)s"%(args.executable, args.input, output_file, titleNumber, args.preset, args.extra_parameters)
    return execute_cmd(extract_cmd)

find_out=find_episodes()
disk_name=get_disk_name(args.input)
series_name=re.sub(r"_S[0-9]+_?D[0-9]+", "", disk_name).title()
if args.output_dir is None:
    args.output_dir="~/Movies/" + series_name

outdir = os.path.expanduser(args.output_dir)
if not os.path.exists(outdir):
    print "Creating directory: %s" % outdir
    os.makedirs(outdir)

titles=[line.replace("+ title ","").replace(":","").strip() for line in (find_out.splitlines()) if line.startswith("+ title")]

print "============================="
print "Series: " + series_name
print "Disk: " + disk_name
print "Titles: " + str(titles)
for title in titles:
    print extract_episode(disk_name, title)
print "Complete"
print "============================="

