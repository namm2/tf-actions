import os, subprocess
from git import Repo

repo = Repo(os.getenv('GITHUB_WORKSPACE'))

diff = repo.index.diff('origin/master')

ignore_dirs = [".github", "modules", "scripts"]

changes = []
for i in diff.iter_change_type('M'):
	file_path = os.path.dirname(i.b_path)
	for name in ignore_dirs:
		if name in file_path:
			break
		changes.append(file_path.strip())

# print(set(changes))
# if not changes:
for d in set(changes):	
	working_dir = os.path.join(repo.working_dir, d)
	print("-------\n", working_dir)
	os.chdir(working_dir)
	
	print("'Running "terraform fmt" ...'", subprocess.run(['terraform', 'fmt', '-diff=true']))
	
	print("'Running "terraform init" ...'", subprocess.run(['terraform', 'init']))
	
	print("'Running "terraform validate" ...'", subprocess.run(['terraform', 'validate']))
