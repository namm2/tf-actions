import os, subprocess
from git import Repo
"""
Github Actions will checkout git repo to env.GITHUB_WORKSPACE directory
Set git Repo to this dir
"""
repo = Repo(os.getenv('GITHUB_WORKSPACE'))

# Diff the current index against refs/origin/master 
diff = repo.index.diff('origin/master')

# List of directories will not be checked by terraform
tf_ignore_dirs = [".github", "docs", "modules", "scripts"]

# Get a list of directories that has changes
changed_dirs = []
for i in diff.iter_change_type('M'):
	file_path = os.path.dirname(i.b_path)
	for d in tf_ignore_dirs:
		if d in file_path:
			file_path = ""
	if file_path != "":
		changed_dirs.append(file_path)

tf_cmds = [
	"terraform fmt -diff=true",
	"terraform init",
	"terraform validate"
]

# Run terraform in a set of directories that has files has changed
for d in sorted(set(changed_dirs)):
	working_dir = os.path.join(repo.working_dir, d)
	print("---------------\n", "Working in:", working_dir)
	os.chdir(working_dir)

	for cmd in tf_cmds:
		print("Run:", cmd)
		print(subprocess.run(cmd, shell=True, text=True, capture_output=True).stdout)

