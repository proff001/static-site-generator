import os
import shutil

def copy_files_recursively(src, dst):
	if not os.path.exists(dst):
		os.mkdir(dst)

	for file in os.listdir(src):
		src_file = os.path.join(src, file)
		dst_file = os.path.join(dst, file)

		if os.path.isdir(src_file):
			copy_files_recursively(src_file, dst_file)
		else:
			shutil.copy(src_file, dst_file)
