## Airavata and PGA Portal Installation Instructions for Ubuntu
The following instructions discuss how to install Airavata and the PGA Portal for development.

### Prerequisites
* Install Docker using the [Ubuntu Instructions](https://docs.docker.com/engine/install/ubuntu/)
    * Follow the [post installation instructions](https://docs.docker.com/engine/install/linux-postinstall/) for Linux to ensure that the docker group is added to your environment.
* Install the docker-compose utility by following the [Linux Instructions](https://docs.docker.com/compose/install/).
* Install Java and set the ```JAVA_HOME``` environment variable within your ```.bashrc``` file.
* Install Intellij IDE for Linux [here](https://www.jetbrains.com/idea/download/#section=linux).
    * Extract the ```tar.gz``` folder
    * Navigate to the ```bin``` directory within the extracted folder
    * Execute the command ```./idea.sh```
    * Follow the installation instructions
* Install maven using the following commands:
    * ```sudo apt update```
    * ```sudo apt install maven```
    * Verify that maven was correctly installed:
    * ```maven -version```
    * Ensure that the output looks similar to this:
    ```
         Apache Maven 3.6.3
         Maven home: /usr/share/maven
         Java version: 15.0.1, vendor: Oracle Corporation, runtime: 
         home/.../.jdks/openjdk-15.0.1
         Default locale: en_US, platform encoding: UTF-8
         OS name: "linux", version: "5.4.0-52-generic", arch: "amd64", family: "unix" ```
* Ensure that Git is installed
* Ensure that Python 3 is installed
* Ensure that npm is installed or up to date.
    * The instructions to install npm can be found [here](https://www.npmjs.com/get-npm)

### Airavata Installation Steps
#### Setting up the development environment
* Clone the Airavata repository or your fork
    * ```git clone https://github.com/apache/airavata```
* [OPTIONAL] If Airavata was installed to the `home` directory, create a new directory called ```airavata_logs```
    * ```mkdir airavata_logs```
* Navigate to the base Airavata directory
    * ```cd airavata```
* Checkout the ```develop``` branch or your respective development branch
    * ```git checkout develop```
* Build the develop branch or your respective development branch
    * ```mvn clean install -DskipTests```
* Build the ```registry-core``` directory
    * ```cd airavata/modules/registry/registry-core```
    * ```mvn clean install -DskipTests```

#### Set up the IntelliJ IDE
* Open the IntelliJ IDE
* Open the ```airavata``` directory as a project
* Configure the project JDK version:
    * Navigate to: ```File -> Project Structure``` and ensure that the project JDK version is set to your Java installation version.
* If Intellij is unable to recognize the plugins when Airavata is opened as a proejct, it is necessary to configure Intellij to recognize the installed plugins:
    * Navigate to ```File -> Settings -> Build, Execution, Deployment -> Build Tools -> Maven```
    * Select the checkbox ```Use plugin registry```
    * Apply these changes
    * Invalidate Caches
        * Select ```File -> Invalidate Caches / Restart...```
* Navigate to the IDE Integration Module in Intellij
    * ```airavata/modules/ide-integration```
* Open the ```APIServerStarter``` class
* Set the VM Options within the Build Configurations
    * Select the ```APIServerStarter``` drop-down menu in the top right section of the Intellij IDE
    * Select ```Edit Configurations```
    * Insert the directory to the JAR file into the ```VM options``` text box.
        * The text provided should be similar to ```-javaagent:/home/.../idea-IC-202.7660.26/lib/idea_rt.jar```
    * Apply the changes
* [OPTIONAL] If the airavata_logs instruction was executed above, reset the Airavata log directory to use the newly created ```airavata_logs``` directory
    * Navigate to ```airavata/modules/configuration/client/src/main/resources/log4j.properties```
    * Reset the line: ```log4j.appender.LOGFILE.File=../../bin/airavata.log``` to ```log4j.appender.LOGFILE.File=~/airavata_logs/airavata.log```

#### Starting backend components (Database, Keycloak, Kafka, RabbitMQ, SSHD Server)
* Add a host entry to ```/etc/hosts``` file in local machine
    * ```127.0.0.1 airavata.host```
* Navigate to ```airavata/modules/ide-integration/src/main/resources```
* Modify the permissions of the ```airavata-php-gateway``` directory
    * Execute the command: ```sudo chmod -R 777 pga/airavata-php-gateway```
* Execute the command: ```docker-compose up -d```
* Apply any database migrations
    * ```cat ./database_scripts/init/*-migrations.sql | docker exec -i resources_db_1 mysql -p123456```
    * [NOTE] It is acceptable if a warning regarding a duplicate table is seen.

#### Start the API Server
* Go to org.apache.airavata.ide.integration.APIServerStarter class and right click on the editor and click Run option. This will start Airavata server

#### Start the Job Execution Engine
* Go to org.apache.airavata.ide.integration.JobEngineStarter class and right click on the editor and click Run option. This will start all components of Job Execution Engine including Helix Controller, Helix Participant, Pre Workflow Manager and Post Workflow Manager.

### Starting the PGA Portal
* Navigate to the ```pga``` directory
    * ```cd pga```
* Execute the command: ```docker-compose up -d```
* Identify the docker IP address
    * ```ip addr```
    * Identify the IP address of the docker container
    * The noteworthy text should look similar to this:
        ```
            4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> 
            mtu 1500 qdisc noqueue state DOWN group default 
            link/ether 02:42:48:e4:f6:56 brd ff:ff:ff:ff:ff:ff
            inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
            valid_lft forever preferred_lft forever```
    * The IP Address of interest, ```172.17.0.1```, is observable next to ```inet``` in this example.
* Update the host entries of pga container with the identified IP address
    * ```docker-compose exec pga /bin/sh -c "echo '<host-machine ip> airavata.host' >> /etc/hosts"```
* Now PGA should be accessible through http://airavata.host:8008
    * Use the username : default-admin and password : 123456 to login to the portal
