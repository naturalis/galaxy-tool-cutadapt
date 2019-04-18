# galaxy-tool-cutadapt
Wrapper for cutadapt, this repo can be used for the new (03-04-2019) galaxy 19.01 Naturalis server. The old galaxy 16.04 server is not supported anymore with this tool. Although cutadapt is also available from the toolshed, this specific wrapper fits better in the pipeline because it can handle zip files.

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
