#!/bin/bash
#!/usr/bin/env python
export PATH=$PATH:/usr/local/sbin

#Configure virtual environment in the scripts 

#virtualenv venv

set -e
source venv/bin/activate

#python3 hello.py

# create a directory data for the extracted data files
mkdir -p data

# create a directory data for the output data files
mkdir -p output

echo "starting to install packages" 
pip install --upgrade pip
pip3 install -r requirements.txt
python -m pip install pika --upgrade
echo "installing laser models might take some time"
python -m laserembeddings download-models
echo "successfully installed all dependencies"

##################
#For extracting data
##################

python scripts/extractdata.py resources/tmx-file.tmx data/data.de data/data.fr
echo "data successfully extracted and stored in the data folder"

##################
#For data cleaning
##################

#use "s/x/y/g" to substitue every pattern x with y and concatenate it "s/x0/y0/g;s/x1/y1/g;s/x2/y2/g"

#expressions filter respectively:
# * <a something >
# * <br \> 
# * </something>
# * <something>
# * <something/>
# * %something
# * Multiple spaces -> single Space
# * Remove space at beginnig of sentence


sed -i.old "s/<a[^>]*>/ /g;s/<br \/>/ /g;s/<\/[[:alpha:]]*>//g;s/<[[:alpha:]]*>//g;/%link/d;s/<[[:alpha:]]*\/>//g;s/&lt\;.*&gt\;//g;s/[[:space:]][[:space:]]*/ /g;s/^[[:space:]]//" data/data.de
sed -i.old "s/<a[^>]*>/ /g;s/<br \/>/ /g;s/<\/[[:alpha:]]*>//g;s/<[[:alpha:]]*>//g;/%link/d;s/<[[:alpha:]]*\/>//g;s/&lt\;.*&gt\;//g;s/[[:space:]][[:space:]]*/ /g;s/^[[:space:]]//" data/data.fr

echo "successfully cleaned the data and saved a copy of the original file with extension .old"



#############################
#DONT UNCOMMENT ( UNDER CONSTRUCT )
#############################

#############################
#For sending data to RabbitMQ
#############################

#to start the rabbitmq server

#brew services start rabbitmq 

#echo "successfully started the rabbitmq-server"

#to start multiple workers

# for i in {1..10};
# do
# 	open -a Terminal ~/Lengoo/FilterMisalignedPairs ; source venv/bin/activate; nohup python3 hello.py >"myprogram_$i.out" 2>&1
# done	


# split - 100 -d --additional-suffix=.txt data/data.de subdata.de

# open -a Terminal ~/Lengoo/FilterMisalignedPairs

#tell app "Terminal" do script "echo hello" end tell

#python rpc_client.py data/data.de data/data.fr