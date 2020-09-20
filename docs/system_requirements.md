## System Requirements
***The RNA Nanostructures Science Gateway shall be referred to as "the system" for the remainder of this document.***

### User-Interface Requirements

1.  The User-Interface (UI) shall be implemented using the Airavata Django Portal, a web interface to the Apache Airavata API.
2.  The UI shall provide a landing page.
    1.  The landing page shall provide high-level information about the RNA Nanostructures Science Gateway project.
    2.  The landing page shall provide a button to enable Users to log in to the system.
        1.  The log-in page shall enable Users to log in using their institution credentials or a registered account.
        2.  The log-in page shall be implemented using CILogon
        3.  CILogon shall be used to require a User to have a registered account.
        4.  CILogon shall be used to verify the validity of a User's credentials.
            1.  CILogon shall reject admission into the application provided invalid credentials.
            2.  CILogon shall enable admission into the application provided valid credentials.
    3.  The landing page shall provide a button to enable Users to register for an account.
        1.  Users shall be required to register with their first name.
        2.  Users shall be required to register with their last name.
        3.  Users shall be required to register with a username.
        4.  Users shall be required to register with a valid email address.
        5.  Users shall be required to register with a valid password.
3.  The User shall be redirected to the available Django Portal upon successful login.
    1.  Should a User login with a valid Administrator account, the User shall be redirected to a management portal.
        1.  The management portal shall provide manager privileges.
            1.  Manager privileges include:
                1.  Implementing new applications
                2.  Modifying existing applications
                3.  Adding additional resources to run applications
                4.  Managing user accounts
                5.  Viewing all jobs and their histories
    2.  Should a User login with a valid User account, the User shall be redirected to a user portal
        1.  The user portal shall provide Users with the ability to perform the following tasks: 
            1.  Select an application to run
            2.  View recently conducted experiments
            3.  Browse experiments
            4.  View the current state of experiments
            5.  Cancel current experiments
            6.  Create new projects
            7.  Edit existing projects
            8.  Upload new files
            9.  Manage files
            10. Download files
            11. Log out from their account
            12. Create new groups
            13. Manage existing groups
            14. Manage group settings
            15. Upload SSH keys
            16. View recent notifications
            17. Email Settings

### RNA Scaffolding Application Requirements
*The RNA Scaffolding Application shall be referred to as "the application".*
1.  The application shall be integrated into the UI.
    1.  The application shall be implemented using Python3.
2.  The application shall require a user to submit a PDB file.
    1.  The application shall verify the integrity of the PDB file.
        1.  The application shall verify the integrity the validity of the PDB file according to the following criteria:
            1.  Filetype ( .pdb)
            2.  Verify by content (ask Joseph about how he does it).
            3.  The PDB file shall be composed of the base pairs to build the RNA 3D scaffold from.
3.  The application shall require a User to enter the starting base pair.
    1.  The starting base pair shall be provided by the User through a text box.
4.  The application shall require a User to enter the end base pair.
    1.  The end base pair shall be provided by the User through a text box.
5. The application shall require a User to enter the number of designs.
    1.  The number of designs shall be provided by the User through a text box.
6. The application shall process the User-provided PDB file using the Design RNA Scaffold application available through RNA Make.
7. The application shall return the a PDB file provided by the Design RNA Scaffold application.
    1.  The returned PDB file shall be downloadable by the User.
    2.  The PDB shall be rendered using JSMol.
        1.  The rendering shall be embedded within the application.
        2.  The rendering shall be viewable in "cartoon" mode.
        3.  The new scaffold built from RNAMake will be highlighted.
8. The application shall return a CSV file provided by the Design RNA Scaffold Application.
    1.  The CSV file shall be displayed in the form of a table.
        1.  The table shall be embedded within the application.

### Airavata Extension Requirements
1.  The Airavata API shall be extended to support job scheduling through HTCondor.
2.  The Airavata API shall be extended to  enable users to submit jobs on the Open Science Grid.
3.  The Airavata API shall be extended to incorporate a Groovy template for HTCondor.
4.  The Airavata API shall be extended to include an HTCondor command map.

### Django Extension Requirements
1.  Be able to send an email to the User.
    1.  The email shall be sent to the email address associated with their account.
    2.  The Django Extension shall be able to send Job Completion emails.
        1.  Job Completion emails shall include the following information:
            1.  Job title
            2.  Associated application
            3.  Time of competition
            4.  Job run time
    3.  The Django Extension shall be able to send Error emails.
        1.  Error emails shall include the following information:
            1.  Job title
            2.  Associated application
            3.  Time of error
            4.  Error messages
2.  The Django Extension shall integrate the API extensions provided by the Airavata Extension as discussed within the Airavata Extension Requirements.
