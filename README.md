# authBioAnalysis
## intro
COMP8920 01 w2021 project
Using machine learning to identify abnormal authentication behavior
### Project structure
web interface
python http server
classifiers
data

## prereq
python3
sklearn
browser(?)
data from https://csr.lanl.gov/data/cyber1/

## download data
download from https://csr.lanl.gov/data/cyber1/
unzip file to /data directory
split/rename files to authpartitionaa - authpartitionzz

### optional: split data with split command
download GNU core utils from http://www.gnu.org/software/coreutils/
add path for the GNU binary
split the auth.txt file into authpartitionaa - authpartitionzz
each sub files with 3000 lines(for example)
>split -l 3000 authpartition

## run project
1 open web.html
2 start server by:
>python3 httpserver.py

## citation
A. D. Kent, “Comprehensive, Multi-Source Cybersecurity Events,”
Los Alamos National Laboratory, http://dx.doi.org/10.17021/1179829, 2015.

@Misc{kent-2015-cyberdata1,
  author =     {Alexander D. Kent},
  title =      {{Comprehensive, Multi-Source Cyber-Security Events}},
  year =       {2015},
  howpublished = {Los Alamos National Laboratory},
  doi = {10.17021/1179829}
}
