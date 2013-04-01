import os
import sys
import commands
import argparse

name_chunks_to_remove=['_UK']

env_handbrake_home = os.getenv('HANDBRAKE_HOME', '__NO_HANDBRAKE_HOME_SET__')
env_handbrake_cli = os.getenv('HANDBRAKE_CLI', env_handbrake_home + '/HandbrakeCLI')

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="The input source", default="/dev/disk1")
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

def execute_cmd(cmd):
    print "Executing " + cmd
    cmd_status, cmd_out = commands.getstatusoutput(cmd)
    if cmd_status != 0:
        print("Failed running %s:"%cmd)
        print(cmd_out)
        print("Exit")
        sys.exit(-1)
    return cmd_out

def find_episodes():
    find_cmd = "%(executable)s -i %(input)s --min-duration %(minimum_minutes)d -t 0"%(vars(args))
    return execute_cmd(find_cmd)

def get_disk_name(device_name):
    disk_name_cmd = "diskutil info " + device_name
    diffutil_out = execute_cmd(disk_name_cmd)
    volume_names=[line for line in diffutil_out.splitlines() if line.strip(" ").startswith("Volume Name")]
    if len(volume_names) == 0:
        raise RuntimeError("Could not find volume name")
    volume_name = volume_names[0].split(":",1)[1].strip()
    for chunk in name_chunks_to_remove:
        volume_name = volume_name.replace(chunk,'')
    print "Found volume name: " + volume_name
    return volume_name

find_out=find_episodes()
disk_name=get_disk_name(args.input)

lines = find_out.splitlines()
titles=[line.replace("+ title ","").replace(":","").strip() for line in lines if line.startswith("+ title")]
print "Found titles: " + str(titles)



print "done"

