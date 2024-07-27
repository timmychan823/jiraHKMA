import requests
import os
import zipfile

class ResourcesManager:
    def __init__(self, output_directory):
        self.output_directory = output_directory

    def downloadFile(self,resources_url,headers,output_file_name):
        r = requests.get(resources_url, headers=headers,stream=True)
        ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
        if not os.path.exists(self.output_directory):
            # Create the directory
            os.makedirs(self.output_directory)
        with open(f"{self.output_directory}/%s.%s" % (output_file_name, ext), 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
            for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
                f.write(chunk) # write the file


    def compress(self):
        lowestDirectory = self.output_directory.split("/")[-1]
        print(lowestDirectory)
        zf = zipfile.ZipFile(f"{lowestDirectory}.zip", "w") #change this later
        for dirname, subdirs, files in os.walk(self.output_directory):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
        zf.close()
    