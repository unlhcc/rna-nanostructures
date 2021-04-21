# Developing Custom Output Viewers
The following documentation serves to provide information regarding the method of extending the existing front-end to support new custom output viewers. As a reference, information will be provided regarding the approach taken to develop the custom `Molecule Viewer` and the custom `Table Viewer` implemented for the RNA Nanostructures Science Gateway.

1. To prepare the Airavata Django Portal to support the new custom output viewer, update the `urls.py` file to include the custom output viewer
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/urls.py` file
    * Append a new URL to the `urlpatterns` list where `your_new_custom_` and `your-new-custom` are replaced with the name of the output view that you wish to implement:
        * `url(r'^pdb-table-output', views.your_new_custom_output_view, name="your-new-custom-output"),`
2. Update the `views.py` to support the new custom output viewer by collecting the required data from the server
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/views.py` file
    * Add a new API View method by following the below pattern. This should be appended to the end of the file (near approximately line 1967). Note that `your_new_custom` should match the name of the output view specified in Step 1.
        * ```
          @api_view()
          def your_new_custom_output_view(request):
              data = _generate_output_view_data(request)
              return Response(data)
          ```

output_views.py (\rna-nanostructures\django_airavata\apps\api\output_views.py)
OutputDisplayContainer.vue (\rna-nanostructures\django_airavata\apps\workspace\static\django_airavata_workspace\js\components\experiment\output-displays\OutputDisplayContainer.vue)
PdbTableOutputDisplay.vue (\rna-nanostructures\django_airavata\apps\workspace\static\django_airavata_workspace\js\components\experiment\output-displays\PdbTableOutputDisplay.vue)