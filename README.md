# DCP
MILESTONE 1
Waterstones bookstore was chosen to extract data from
A class was created to scrape data
Method to accept cookies, scroll to the bottom, load all the books and collect their respective links was added 

MILESTONE 2
Created function to retrieve text and image data from the sites. 
Generated unique ID's for each product then organised it into a list of dictionaries. 
The raw data is stored locally in folders for each product. 
The pictures are also downloaded and stored in their respective folders. 
There was an issue using urlib and so I had to use requests library.

MILESTONE 3 
Extracted text and images links for each book. 
Generated unique id's for each book. 
Organise the data into a list of dictionaries. 
Download the image links.
Save the data of each book into their respective folders organised by the ISBN number. 

MILESTONE 4 
Generate a unit test file in order to check the datatypes of the outputs of each method in the Scraper class. 
Generate a integration test file in order to check the file integrety of the saved data

MILESTONE 6
Uploaded raw data into s3 bucket using boto3
Uploaded tabular data to RDS using psycopg2 and sqlalchemy
Option to upload image data directly to s3

MILESTONE 7
prevent rescraping

MILESTONE 8 
Run scraper in headless mode. 
Create dockerhub image
Push the container to the dockerhub
Pull the image and run the scraper in the EC2 instance. 

MILESTONE 9
Set-up Prometheus to monitor the scraper and ec2 instance. 
set-up Gradana to monitor the metrics 

MILESTONE 10 

Setup GitHub secrets to connect the repo to the dockerhub image
Created GitHub action to create and push the new image everytime there is a push to the main branch 
Created cron jobs on the ec2 instance to kill the container, download the new image and run it everyday