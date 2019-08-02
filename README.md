# cgccli
The Cancer Genomics Cloud command line tool

Run `python setup.py install` in order to install the package
Run `pip uninstall cgccli` in order to uninstall the package


# CGC command line tool
The Cancer Genomics Cloud (CGC), powered by Seven Bridges, is one of three pilot
systems funded by the National Cancer Institute to explore the paradigm of colocalizing
massive genomics datasets, like The Cancer Genomics Atlas (TCGA), alongside secure
and scalable computational resources to analyze them.
You need to write CLI tool for CGC Public API (docs:
https://docs.cancergenomicscloud.org/docs/the-cgc-api)
CLI tool should support following operations:
1. List projects (https://docs.cancergenomicscloud.org/docs/list-all-your-projects)
2. List files in project
(https://docs.cancergenomicscloud.org/docs/list-files-in-a-project)
3. Get file details (https://docs.cancergenomicscloud.org/docs/get-file-details)
4. Update file details
(https://docs.cancergenomicscloud.org/docs/update-file-details)
5. Download file
(https://docs.cancergenomicscloud.org/docs/get-download-url-for-a-file)
Sample usage:
cgccli --token {token} projects list
cgccli --token {token} files list --project
test/simons-genome-diversity-project-sgdp
cgccli --token {token} files stat --file {file_id}
cgccli --token {token} files update --file {file_id} name=bla
cgccli --token {token} files update --file {file_id}
metadata.sample_id=asdasf
cgccli --token {token} files download --file {file_id} --dest
/tmp/foo.bar
Doing this homework you will need to
1. Register account on www.cancergenomicscloud.org/
2. Get your authentication token
3. Create test projects by copying some of Public projects (ex:

a. https://cgc.sbgenomics.com/u/sevenbridges/personal-genome-project-uk-
pgp-uk/

b. https://cgc.sbgenomics.com/u/sevenbridges/simons-genome-diversity-proj
ect-sgdp

You can pick any Python framework / library that you like, there are no preferences
whatsoever on our side.
Thank you so much for taking the time to complete the task! When you are ready with
the task please send us back a github link to the repository or the archived folder. Our
team will evaluate it and we will hear soon with the team feedback. Please feel free to
reach to us for additional
