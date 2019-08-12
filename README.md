# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

#iniciar con este comando
sudo sysctl -w vm.max_map_count=262144

#matar todos los contenedores
docker kill $(docker ps -q)

#generar certificados para comunicación interna de -kibana (ejecutar una sóla vez)
docker-compose -f create-certs.yml run --rm create_certs

docker-compose -f create-certs.yml run --rm create_certs

docker-compose run --rm create_certs


TAg=.env docker-compose config

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact