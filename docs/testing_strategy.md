# Testing Strategy
The project uses distinct testing strategies for the different frameworks.

### Airavata
- The Airavata server API system makes use of unit tests in a number of portions of the code which are run during Maven builds as well as run using Travis CI on the apache/airavata repository; however, testing the full stack of services to confirm usability of the workflow manager and job submission system does not employ any mock or unit testing. This is as set up by Apache/Airavata and consequently the testing strategy cannot be modified by the team.
- The Airavata-HTCondor Extension is manually tested using the following components:
  - Docker to spin up the required backend services such as the databases and credential broker.
  - The Airavata API, job manager, and job monitor--started in the IDE.
  - A virtual machine running Ubuntu with HTCondor and an SMTP server are installed.
    - The above tools are used to run a testing pool and to send job notifications to our test email that the job monitor polls.
  - The PGA portal after spinning it up using Docker as per the testing instructions.
    - The steps to configure the PGA Portal on a Linux environment can be found [here](https://github.com/cseseniordesign/rna-nanostructures/blob/master/docs/testing/pga_portal_installation_instructions.md).
    - While in the default Super Admin mode of the PGA Portal, the virtual machine compute resource is registered.
    - After disabling the Super Admin mode in the PGA Portal, the virtual machine compute resource is set up with the default gateway and set to default.
  - The Django Portal with the following configurations:
    - The settings are configured to all point to the local Docker services and local running Airavata API service.
    - The compute resource is registered in the settings portion of the Django portal.
    - An application is set up to run on the compute resource.
  - An application is then tested using the virtual compute resource. If the application is able to complete successfully and the output on the IDE console running the Airavata services does not indicate any failures, we consider it in the working state. Otherwise, we edit code/settings/configurations to fix the issues we ran into.

### Django
- The Airavata Django Portal makes use of unit testing via Django framework, testing sub-components according to the unit tests employed. It also performs Python style and syntax validation through `flake8`. This is tested using Travis CI which runs the Django tests and yarn tests for the server.
- Travis CI performs continuous integration on every commit and pull request, making sure code can be merged.
- The PDB parser is tested using the same Django test suite, which allows it to be tested using the same testing system.
