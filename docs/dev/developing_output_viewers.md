# Developing Custom Output Viewers
The following documentation serves to provide information regarding the method of extending the existing front-end to support new custom output viewers. As a reference, information will be provided regarding the approach taken to develop the custom `Molecule Viewer` and the custom `Table Viewer` implemented for the RNA Nanostructures Science Gateway.

1. For all viewers that will require any `npm` dependencies, the file `rna-nanostructures/django_airavata/apps/workspace/package.json` should be updated to include the respective package and the version to be used in the application. This can be done by using the command `yarn add dependancy` where `dependancy` is the name of the `npm` package name within the location `rna-nanostructures/django_airavata/apps/workspace`.
2. Update the `views.py` to support the new custom output viewer by collecting the required data from the server
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/views.py` file
    * Add a new API View method by following the below pattern. This should be appended to the end of the file (near approximately line 1967).
        * ```
          @api_view()
          def your_new_custom_output_view(request):
              data = _generate_output_view_data(request)
              return Response(data)
          ```
        * **NOTE:** Replace `your_new_custom_` with the name of the new custom output viewer that will be added
3. To prepare the Airavata Django Portal server to support the new custom output viewer, update the `urls.py` file to include the custom output viewer
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/urls.py` file
    * Append a new URL to the `urlpatterns` list where `your-new-custom` are replaced with the name of the output view that you wish to implement and `your_new_custom_` is replaced with the naming used:
        * `url(r'^your-new-custom-output', views.your_new_custom_output_view, name="your-new-custom-output"),`
        * **NOTE:** Ensure that the `name` element and the element following `r'^` are equivalent
4. Create a new file to contain the custom output view
    * Create a new output display `Vue` file within the `rna-nanostructures/django_airavata/apps/workspace/static/django_airavata_workspace/js/components/experiment/output-displays/` directory (e.g., `YourCustomOutputDisplay.vue`)
5. Add a new custom output data type to the Output Display Container
    * Navigate to the `rna-nanostructures/django_airavata/apps/workspace/static/django_airavata_workspace/js/components/experiment/output-displays/OutputDisplayContainer.vue` file
    * Update the imports specified on approximately lines 31-41 to include the file created in Step 4. The name of the class imported from the file should be equivalent to the name of the file, but the `.vue` element will be removed.
    * Update the `components` on approximately lines 64-74 to include the imported class specified in the previous step
    * Append a new data type to the `displayTypeData()` object on approximately line 96 using the following format where the name of the component is equivalent to the component name previously specified; however, the name formatting should be modifed to be dash-separated lowercase.
        * ```
          custom_output: {
            component: "your-custom-output-display",
            url: "/api/your-new-custom-output/",
          }
        * **NOTE:** The element of the URL following `/api/` in the above code should be equivalent to the name of `your-new-custom-output` used in Step 1.
6. Implement an output view provider to enable access to the output view implementation
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/output_views.py` file
    * Implement a new output view provider by creating a dictionary with the desired elements. For situations requiring an output file, the `output_file` parameter has been provided. The following code snippet provides reference to the approach that may be taken to implement this provider.
        * ```
          class YourCustomViewProvider:
            display_type = 'custom_output'
            name = 'Your Custom Output'

            def generate_data(self, request, experiment_output, experiment, output_file=None, **kwargs):
                return {
                    'key': output_file
                }
        * **NOTE:** Replace the `display_type` value with the name of the object specified in Step 5 (i.e., `custom_output`); replace the `name` value with the name of the custom output viewer as you desire it to be presented to the User; update the dictionary returned in the `generate_data()` method to include the data that you wish to utilize for the custom output viewer.
7. Implement the output viewer
    * Within the new file created for Step 4, create a new `<template>` to embed the output view within. References for this can be observed within the alternative existing output views. Note that the template should be implemented for the type of output that you wish to display to the user (e.g., an image).
    * In the new file, create a new `<script>` that will contain the implementation to create the desired output view and update the `template` to present this to the User
    * **NOTE:** The `<script>` should access the desired data with the expectation that the provided data will be provided as implemented in the dictionary created in Step 4. That is, the keys and value established in Step 4 will also be accessible in the implementation for the output viewer. References to approaches that may be taken to implement an output viewer are available in the other output view files in the current directory (e.g., `PdbTableOutputDisplay.vue`). Finally, the name of the object implemented within the `<script>` should be equivalent to the name of the component that was established in Step 3. (i.e., what you changed `your-custom-output-display` to be)

### References
The University of Nebraska-Lincoln Senior Design Team implemented two new custom output viewers for their project. The locations of the files changed and their respective files are documented below:
* GLMol Output Viewer
    * File: `rna-nanostructures/django_airavata/apps/api/views.py`
    * File: `rna-nanostructures/django_airavata/apps/api/urls.py` 
    * File: `rna-nanostructures/django_airavata/apps/workspace/static/django_airavata_workspace/js/components/experiment/output-displays/OutputDisplayContainer.vue` 
    * File: `rna-nanostructures/django_airavata/apps/workspace/static/django_airavata_workspace/js/components/experiment/output-displays/MoleculeOutputDisplay.vue`
    * File: `rna-nanostructures/django_airavata/apps/api/output_views.py`
    * Imports: 
        * File: `rna-nanostructures/django_airavata/static/glmol/ChemDoodleWeb.js`
        * File: `rna-nanostructures/django_airavata/static/glmol/ChemDoodleWeb.css`
        * File: `rna-nanostructures/django_airavata/apps/workspace/templates/django_airavata_workspace/view_experiment.html`
* PDB Table Viewer
    * File: `rna-nanostructures/django_airavata/apps/api/views.py`
    * File: `rna-nanostructures/django_airavata/apps/api/urls.py` 
    * File: `rna-nanostructures/django_airavata/apps/workspace/static/django_airavata_workspace/js/components/experiment/output-displays/OutputDisplayContainer.vue` 
    * File: `rna-nanostructures/django_airavata/apps/workspace/static/django_airavata_workspace/js/components/experiment/output-displays/PdbTableOutpuDisplay.vue`
    * File: `rna-nanostructures/django_airavata/apps/api/output_views.py`
    * Imports: `rna-nanostructures/django_airavata/apps/workspace/package.json`

Additional documentation for development and setup for custom output viewers can be found [here](https://github.com/cseseniordesign/rna-nanostructures/blob/master/docs/dev/custom_output_view_provider.md)
