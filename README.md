# galaxy-tool-cutadapt
wrapper for cutadapt
## Getting Started
### Prerequisites
Cutadapt need to be installed. Below are instruction to install cutadapt.
```
pip install --user --upgrade cutadapt
```
```
sudo ln -s ~/.local/bin/cutadapt /usr/local/bin/cutadapt
```
Check the version, this should be at least version 1.6
```
cutadapt --version
```
### Installing
Installing the tool for use in Galaxy
```
cd /home/galaxy/Tools
```
```
sudo git clone https://github.com/naturalis/galaxy-tool-cutadapt
```
```
sudo chmod 777 galaxy-tool-cutadapt/cutadapt_wrapper.py
```
```
sudo ln -s /home/galaxy/Tools/galaxy-tool-cutadapt/cutadapt_wrapper.py /usr/local/bin/cutadapt_wrapper.py
```
```
sudo cp galaxy-tool-cutadapt/cutadapt.sh /home/galaxy/galaxy/tools/identify/cutadapt.sh
sudo cp galaxy-tool-cutadapt/cutadapt.xml /home/galaxy/galaxy/tools/identify/cutadapt.xml
```
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="identify/cutadapt.xml" />
```
## Source

Martin, M. (2011). Cutadapt removes adapter sequences from high-throughput sequencing reads. EMBnet.Journal, 17(1), pp. 10-12. doi:http://dx.doi.org/10.14806/ej.17.1.200
