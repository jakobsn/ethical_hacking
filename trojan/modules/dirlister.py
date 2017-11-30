import os
def run(**args):
	print "[*] In dirlister module."
	files = os.listdir(".")
	print "[*] Content"
	print files
	return str(files)
