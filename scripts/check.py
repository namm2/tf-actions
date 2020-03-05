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

change_dirs = []
for i in diff.iter_change_type('M'):
	file_path = os.path.dirname(i.b_path)
	for name in tf_ignore_dirs:
		if name in file_path:
			continue
		change_dirs.append(file_path.strip())

# print(set(changes))
# if not changes:
for d in set(change_dirs):	
	working_dir = os.path.join(repo.working_dir, d)
	print("-------\n", working_dir)
	os.chdir(working_dir)
	
	print(subprocess.run("terraform fmt -diff=true", shell=True, text=True, capture_output=True).stdout)
	
	print(subprocess.run("terraform init", shell=True, text=True, capture_output=True).stdout)
	
	print(subprocess.run("terraform validate", shell=True, text=True, capture_output=True).stdout)
