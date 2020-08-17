# ElasticPanda  <img src="logo.png" alt="alt text" width="302px" height="100px">
<a href='https://www.freepik.com/vectors/logo' style="font-size:5px">Original logo vector created by sentavio - www.freepik.com</a>
## Elasticsearch search engine supercharged with Python Pandas.
Search Engine, based on **Elasticsearch** aided by **Python Pandas** data manipulation package.

### Components:
 - **Elasticsearch**: Two-node Elasticsearch 7.2 Cluster, with native [REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html) available in its endpoint.
 - **Nginx:** Nginx service built from [Nginx official Docker image](https://hub.docker.com/_/nginx). Used for enabling **https** on Kibana and Jupyter endpoints, and Elasticsearch REST API.
 - **Certbot:** Custom docker container for configuration of **https** SSL certificates, and automating its renewal. Based on [nginx-certbot project](https://github.com/wmnnd/nginx-certbot)
- **Flask:** Flask container, with **Pandas** library installed, based on (c) 2019 Dinesh Sonachalam [Elasticsearch-Flask Tutorial](https://github.com/dineshsonachalam/Building-a-search-engine-using-Elasticsearch)

### Dependencies
 - Docker and Docker-compose.
 - node.js
 - npm
 - elastic dump [see install instructions](https://www.npmjs.com/package/elasticdump) 

## Setup 
 1. Create `.env` file and populate environment variables.Follow structure outlined in the [example .env file](example.env)
 2. `./app-init.sh`--->Create the folders and change permissions necessary for **ElasticPanda** startup.
 3. Register 2 domains, for the Flask App and Elasticsearch endpoints,all pointing to your **server/VM IP**.
 4. Change accordingly the environment variables on the `.env` file.
 5. `./certbot.sh`--->Create the SSL certificates and keystores for enabling **https** on the Flask app endpoint and the Elasticsearch REST API.
 6. `docker-compose up search`--->Start only the Flask App (used for when connecting to an external Elasticsearch URL for example)


## Startup
 1. `docker-compose up`--->Start the stack
 2. `docker-compose up docker-compose_local.yaml`---->Start the stack in local mode (without nginx nor certbot, for testing in local environment).
 3. `docker-compose up --build`--->Start the stack recreating the services after changes in environment variables.
 4. `docker-compose up flask`--->Start the stack recreating the services after changes in environment variables.

## File Structure

Relevant File structure
```
📦EJK
┣ 📂args
┃ Folder for python arguments, including elasticsearch queries.
┣ 📂flask_app
┃ Flask container configuration files, including Dockerfile, app script and templates.
┣ 📂modules
┃  Custom python modules and classes.
┣ 📂nginx
┃  Nginx configuration files, including Dockerfile.
┃ ┣ 📂conf
┃ ┃ ┣ 📜nginx-docker-entrypoint.sh
┃ ┃ ┃   Script executed at nginx container startup. It substitutes parameters from .env file in virtual server configuration file.
┃ ┃ ┗ 📜nginx.conf.template
┃     Virtual server configuration file.
┣ 📜app-init.sh
┃   Stack setup script.
┣ 📜certbot.sh
┃    Certbot setup script.
┣ 📜docker-compose.yml
┃    Stack docker-compose file.
┣ 📜.env
┃    .env file for docker-compose file.
```
## TROUBLESHOOTING:
