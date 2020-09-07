import os
import os.path
import glob

link_list_dir = "link_list.txt"		# This folder contains all of our media links
tmp_dir = "output/tmp"  # This folder is our work folder
output_dir = "output/"			# This folder is our main output folder

# Create required folders
if not os.path.isfile(link_list_dir):
	open(link_list_dir,"w+")
	print("[Creation] No link list file, created one!")

if not os.path.exists(output_dir):
	os.mkdir(output_dir)
	print("[Creation] No output file, created one!")

if not os.path.exists(tmp_dir):
	os.mkdir(tmp_dir)
	print("[Creation] No tmp file, created one!")

# Go though the file list line by line to get links
with open(link_list_dir, 'r') as link_list:
	for line in link_list:
		print("[youtube-dl] Downloading " + line.rstrip())

		# Download the icon and audio using youtube-dl
		os.system("youtube-dl -q --write-thumbnail --audio-quality 0 --audio-format 'mp3' --output '"+tmp_dir+"/%(title)s.%(ext)s' --add-metadata --metadata-from-title '%(artist)s - %(title)s' -x " + line + " > /dev/null")

		# Find the files and assign them into a variable
		files = glob.glob(tmp_dir+ "/*.*")
		for file in files:
			if ".mp3" in file:
				audio_file = repr(file)
			else:
				image_file = repr(file)

		# Convert the image into a format we can use
		os.system("ffmpeg -loglevel panic -i " + str(image_file) + " " +tmp_dir+ "/thumbnail.png")
			
		image_file = tmp_dir + "/thumbnail.png"
		print("[Image] Converted image")

		# Add icon and move it to the output directory
		os.system("ffmpeg -loglevel panic -i " + audio_file + " -i " + image_file + " -map 1 -map 0 -c copy -disposition:0 attached_pic -y -f 'mp3' " + audio_file.replace("/tmp", ""))
		
		# Delete files in the tmp directory to make room for our next media
		files = glob.glob(tmp_dir + "/*.*")
		for file in files:
			os.system("rm " + repr(file))
			print("[Cleanup] Removed " + repr(file))

os.system("rm -d " + repr(tmp_dir))
print("[Finished] The end of the file has been reached!")