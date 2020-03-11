# galaxy-tool-cutadapt
Wrapper for Cutadapt v.2.8. This repo supports Python3 and has been tested with Galaxy v.19.09 (expected to work with Galaxy v.20 as well). In contrast to cutadapt from the toolshed, this wrapper will handle zip files.

## Getting Started
### Installing
Installing the tool for use in Galaxy

execute the following commands as user galaxy
```
cd /home/galaxy/Tools
```
```
git clone https://github.com/naturalis/galaxy-tool-cutadapt
```
```
chmod 777 galaxy-tool-cutadapt/cutadapt_wrapper.py
```
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="/home/galaxy/Tools/galaxy-tool-cutadapt/cutadapt_primer_trim.xml" />
```
## Source

Martin, M. (2011). Cutadapt removes adapter sequences from high-throughput sequencing reads. EMBnet.Journal, 17(1), pp. 10-12. doi:http://dx.doi.org/10.14806/ej.17.1.200
