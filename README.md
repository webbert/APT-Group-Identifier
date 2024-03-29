# APT-Group-Identifier

Advanced Persistent Threats are highly skilled cyber hacker groups. These different groups have many ways of performing attacks. By using Webscraping, MITRE ATTACK Framework and Machine learning, we will test and determine whether we are able to identify the group by their type of activity.

## Basic Instructions

This package uses webscraping to siff out the details from the website. The main scraper it is using is beautifulsoup from bs4.

## Installation

There are a few package dependencies that need to be installed.

```shell
python -m pip install < requirments.txt
```

## Instructions for use [APT_Info]

Importing APT_Info module from MITRE.

```python
from MITRE import APT_Info
```

### Displaying all basic information of APT Groups

```python
apt_info_obj = APT_Info()
result_df = apt_info_obj.all()
# Returns a Pandas.Dataframe with all the information
```

Refer to "csv results" folder, all APT groups basic information.

### Displaying all the information of the specific APT group

```python
apt_info_obj = APT_Info()
apt_dragonfly_dictionary = apt_info_obj.display_apt_info("G0035") # Dragonfly Group Code
# Dictionary contains different headers of the APT
```

Refer to csv files with "Dragonfly", all APT groups basic information.

## Addtional test

Digital Forensics Specialist and Threat Hunting Analysts has always determine an APT cyber espionage by distinguishing their TTPs (Tatics, Techniques and Procedures). 

I have tested by using machine learning to train a model to see whether I can determine the APT group by the techniques used. I

For this Proof Of Concept, I used DecisionTreeClassifier as a model. Further testing should be dibe as the current results does not seem to be accurate.

Execute train_mode.py, followed by ProofOfConcept.py.
Do refer to ProofofConcept python script to execute.