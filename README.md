# galaxy-tool-cutadapt
Wrapper for Cutadapt v.2.8. This repo supports Python3 and has been tested with Galaxy v.22.01.  
In contrast to cutadapt from the toolshed, this wrapper will handle zip files.

## Installation
### Manual
Clone this repo in your Galaxy ***Tools*** directory:  
`git clone https://github.com/naturalis/galaxy-tool-cutadapt`  

Make the python script executable:  
`chmod 777 galaxy-tool-cutadapt/cutadapt_wrapper.py`  

Append the file ***tool_conf.xml***:    
`<tool file="/path/to/Tools/galaxy-tool-cutadapt/cutadapt_primer_trim.xml" />`

### Ansible
Depending on your setup the [ansible.builtin.git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html) module could be used.  
[Install the tool](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html#examples) by including the following in your dedicated ***.yml** file:  

`  - repo: https://github.com/naturalis/galaxy-tool-cutadapt`  
&ensp;&ensp;`file: cutadapt_primer_trim.xml`  
&ensp;&ensp;`version: master`  

## Source

Martin, M. (2011). Cutadapt removes adapter sequences from high-throughput sequencing reads. EMBnet.Journal, 17(1), pp. 10-12. doi:http://dx.doi.org/10.14806/ej.17.1.200
