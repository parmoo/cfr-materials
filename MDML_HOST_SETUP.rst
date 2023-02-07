# Setting up an MDML Host
An MDML host and its services can be quickly spun up using docker compose. 
Once the host is running, any mdml client created through the mdml_client python package will be able to connect and start streaming data. 
The compose files and directions for setup are contained within the [mdml-minimal repo](https://github.com/anl-mdml/mdml-minimal).
Assuming docker-compose is installed on the host machine, MDML hosts only require a few environment variables be specified before starting.
