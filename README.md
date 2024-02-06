# Oystor - Oyster Storage and Visualization Tool 
This is the backend code for my Oystor project. It is a basic Flask api with a few routes. I have kept my routes to a minimum at this point as this is a growing project. In order to run this program there is an up to date requirements.txt file available to download all dependencies. You will have to start a PostgreSQL database server on your local device as well. I have provided two .sql files with which you can seed your database. The information within is pertinent only to the farm for which I currently work. If you are familiar with SQL and want to modify or create your own files feel free. All of the data here is public knowledge.
## Starting your server
Once you have created your database and started the PSQL server, you can clone the repository and start your local Flask server using the command 'flask run'. This will not generate any feedback in your browser but if you want to check its status you can either go directly to [http://localhost:5000](http://localhost:5000) or you can cURL that URL using the curl command or your favorite tool such as Insomnia. 
## Frontend
Once your server is up and running you will have to go to the frontend repository located here https://github.com/pllomba90/wetStorage-frontend and clone it. Other information is located there. 