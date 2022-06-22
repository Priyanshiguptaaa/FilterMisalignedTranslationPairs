# FilterMisalignedTranslationPairs

### Table of Contents
1. [About](#about)
2. [System Overview](#system-overview)
3. [Installation & Implementation](#installation-and-implementation)
4. [Results](#results)
5. [Proposal for Scaling](#proposal-for-scaling)

### About

Misalignment, i.e., parallel sentence pairs that are not accurate translations of each other, is a common problem that occurs even in well-curated datasets. This project is focused on making a prototypical cleaner to exploit sentence embeddings to filter misaligned segment pairs 

### System Overview

<img align='center' src="https://github.com/Priyanshiguptaaa/FilterMisalignedTranslationPairs/blob/main/diagrams/system.png" width="700" height="680">


### Installation and Implementation

#### 1. Clone the repo

```bash
git clone https://github.com/lengoo/research-engineer-coding-challeng-Priyanshiguptaaa.git
```

#### 2. Navigate to the working directory

```bash
cd research-engineer-coding-challeng-Priyanshiguptaaa/
```

#### 3. Create a virtual environment and activate it

```bash
virtualenv venv
source venv/bin/activate
```

#### 4. To install RabbitMQ server

For MacOS

```bash
brew update
brew install rabbitmq
```
For your desired platform:
Check this link : https://www.rabbitmq.com/download.html

#### 5. Run the bash script run.sh for dependencies installation, data extraction and data cleanining 

** Note: You can uncomment the code blocks in the run.sh file according to your current requirements

```bash
bash run.sh
```

#### Inside run.sh

- Installing dependencies

```bash

pip install --upgrade pip
#installing the libraries mentioned in requirements.txt
pip3 install -r requirements.txt
#installing pika
python -m pip install pika --upgrade
#installing the laser models
python -m laserembeddings download-models

```

- For extracting data from a tmx file

```bash
python scripts/extractdata.py resources/tmx-file.tmx data/data.de data/data.fr
```

- For cleaning data

Use cases taken care of:

```
- * <a something ></a>
- * <br \> 
- * </something>
- * <something>
- * <something/>
- * %something
- * Multiple spaces -> single Space
- * Remove space at beginnig of sentence
```
bash command to run for cleaning the text files

```bash
sed -i.old "s/<a[^>]*>/ /g;s/<br \/>/ /g;s/<\/[[:alpha:]]*>//g;s/<[[:alpha:]]*>//g;/%link/d;s/<[[:alpha:]]*\/>//g;s/&lt\;.*&gt\;//g;s/[[:space:]][[:space:]]*/ /g;s/^[[:space:]]//" data/data.de
sed -i.old "s/<a[^>]*>/ /g;s/<br \/>/ /g;s/<\/[[:alpha:]]*>//g;s/<[[:alpha:]]*>//g;/%link/d;s/<[[:alpha:]]*\/>//g;s/&lt\;.*&gt\;//g;s/[[:space:]][[:space:]]*/ /g;s/^[[:space:]]//" data/data.fr
```

#### 6. Starting the RabbitMQ server

```bash
brew services start rabbitmq 
```

#### 7. Open up 4 terminals for 4 workers to consume the data  

** Note: You can add or reduce the number of consumers according to the number of terminals you open

Navigate to your working directory and execute the following commands:

```bash
source venv/bin/activate
python3 scripts/worker.py
```
The terminal shows:

" [x] Awaiting Language Pairs, To exit press CTR+C"

** Note: You have to press CTR+C for all the consuming terminals after the client.py script completes execution and the command line exits 

#### 8. Open up another terminal for running the client script and sending data to the server

** Note: Provide the directories in the command according to the data you want to send

Navigate to your working directory and execute the following commands:

```bash
source venv/bin/activate
python3 scripts/client.py data/data.de data/data.fr
```
#### 9. To see some insights into the results

Note: Pass these as arguments 

- file with the filtered data
- file with the initial data
- similarity score value based on which you classify pair as aligned or misaligned

```bash
python3 scripts/filtereddataanalysis.py output/filtereddata.de data/data.de 0.80
```


### Results

```
Analysis for filtering based on similairty score: 0.80
Total langauge pairs : 1449
Aligned langauge pairs : 70
Percentage of aligned langauge pairs : 4.830917874396135 %
```

```
Analysis for filtering based on similairty score: 0.75
Total langauge pairs : 1449
Aligned langauge pairs : 188
Percentage of aligned langauge pairs : 12.974465148378192 %
```

### Proposal for Scaling

While we execute a product or service locally, there are several issues that must be considered when using local hardware or CPU. The purpose of scaling is to design the service in such a way that it can operate optimally even when the data load or traffic grows. We must also ensure that no single worker is overburdened; otherwise, they may crash due to unforeseen circumstances.

Potential inclusions in the software when scaling:

- Include end-to-end tests to ensure that the service does not fail or operate poorly at any phase. 
- Include data validation tests to ensure that the data is clean and contains the qualities required by the service.
- When deploying the service, include the processes in a CI/CD pipeline. Building, packaging, testing, validating, certifying infrastructure, and deploying to all required environments are among them.
- After the data extraction and cleaning, add an approval phase to ensure that no use cases for cleaning are missing.
- Figure out the number of workers needed to scale the service.
- Enable worker auto scaling so that we may skip unnecessary processes while the queue size is small and add more processes when the number of waiting messages grows.



