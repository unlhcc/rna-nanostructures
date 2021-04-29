# Developing a Custom Input Validator
The Airavata Django Portal integrates validation for both text input and file validation. The following documentation serves to discuss the instructions to implement a new custom input validator.

The first step in implementing a new validator is to determine the input for the validator. If the input will be text from a text-box, it will be necessary to implement a validator to handle text input. If the input will be a file (e.g., a PDB file), it will be necessary to both implement a file validation script and to extend the implementation to support this new validation method. To learn how to implement a text input validator, refer to the [Text Input Validator Instructions](#text-input-validator-instructions). To learn how to implement a file input validator, refer to the [File Input Validator Instructions](#file-input-validator-instructions)

## Text Input Validator Instructions
The following instructions serve to discuss the method of developing a new text input validation method.

1. Create a new `javascript` file that will house the custom validator
    * Navigate to the directory `rna-nanostructures/django_airavata/apps/api/static/django_airavata_api/js/models/validators/`
    * Create a new `javascript` file that will contain the validator for the provided input
        * For example, `MyCustomValidator.js` where, `MyCustomValidator` is the name of the validator that will be made and will become the name of the validator class.
2. Create a new option in the `Validator Factory`
    * Naviagate to the file `rna-nanostructures/django_airavata/apps/api/static/django_airavata_api/js/models/validators/ValidatorFactory.js`
    * Import the new validator created in Step 1 into the `ValidatorFactory.js` file
        * `import MyCustomValidator from "./MyCustomValidator";`
        * **NOTE:** Replace MyCustomValidator with the name of the validator that has been specified in Step 1.
    * Add a new reference entry to the `VALIDATOR_MAPPING` object
        * `custom_validator: MyCustomValidator,`
        * **NOTE:** Replace `custom_validator` with the name of the validator as you wish Users to reference it in the front-end configuration
3. Implement the input editor to validate the text input as desired
    * Navigate to the file created in Step 1.
    * Create the validator to validate the input using the desired configurations and the desired output messages. It is worth noting that the essential components are the `validate()` function, and the `MyCustomValidator` class, where `MyCustomValidator` is replaced with the naming scheme established for Step 1.
    * As a reference, the following skeleton code has been provided. For additional references, refer to the `MaxLengthValidator.js` file or the `MinLengthValidator.js` file.
        * ```javascript
          export default class MyCustomValidator {
            constructor(config) {
                // Here you should collect any configurations that you desire (i.e., the minimum length of the text input)
                this.myConfig = config["value"];
                if ("message" in config) {
                  this.customErrorMessage = config["message"];
                }
            }

            validate(value) {
                if (value === null || typeof value === "undefined") {
                  return this.getErrorMessage(value);
                }
                if (typeof value !== "string") {
                  value = value.toString();
                }

                // Validate the text input here and return the error message
                if (valid) {
                 return this.getErrorMessage(value);
                }
                
                return null;
            }

            getErrorMessage() {
                if (this.customErrorMessage) {
                  return this.customErrorMessage;
                } else {
                  return ("This is my default error message");
                }
            }
          }
          ```

## File Input Validator Instructions
The following instructions serve to discuss the approach that should be taken to implement a file input validator. These instructions assume that a file validation script has already been implemented. If a file validation script has not yet been implemented, please do so prior to completing the following instructions. Refer to the `pdb_parser.py` file as an example.

1. Create a new `javascript` file that will house the custom validator
    * Navigate to the directory `rna-nanostructures/django_airavata/apps/api/static/django_airavata_api/js/models/validators/`
    * Create a new `javascript` file that will contain the validator for the provided input
        * For example, `MyCustomValidator.js` where, `MyCustomValidator` is the name of the validator that will be made and will become the name of the validator class.
2. Create a new option in the `Validator Factory`
    * Naviagate to the file `rna-nanostructures/django_airavata/apps/api/static/django_airavata_api/js/models/validators/ValidatorFactory.js`
    * Import the new validator created in Step 1 into the `ValidatorFactory.js` file
        * `import MyCustomValidator from "./MyCustomValidator";`
        * **NOTE:** Replace MyCustomValidator with the name of the validator that has been specified in Step 1.
    * Add a new reference entry to the `VALIDATOR_MAPPING` object
        * `custom_validator: MyCustomValidator,`
        * **NOTE:** Replace `custom_validator` with the name of the validator as you wish Users to reference it in the front-end configuration
3. Create a new method to handle collecting the User-provided file and to validate the file using the implemented file validation script.
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/views.py` file
    * Import the `validation()` method responsible for validating a file
        * For example, the `validate_pdb()` method provided in the `pdb_parser.py` file
    * Create a new validation method at the bottom of the file that will be responsible for collecting the User-provided file and for calling the `validation()` method imported. Use the following template to implement this method. Note that the method name `file_validation()` can be modified to your desired naming.
        * ```python
          def file_validation(request):
            # Get the data product URI that contains the User-provided file
            data_product_uri = request.GET['dataProductURI']
            try:
                data_product = request.airavata_client.getDataProduct(request.authz_token, data_product_uri)
            except Exception as e:
                log.warning("Failed to load DataProduct for {}"
                            .format(data_product_uri), exc_info=True)
                # The system was unable to collect the specified data product URI
                raise Http404("data product does not exist") from e
            # Attempt to validate the file using the provided validation method
            try:
                # Create the new Python file object using the built-in API open_file method
                file = user_storage.open_file(request, data_product)

                # Validate the file and collect the errors returned
                # TODO: Replace the validate_file() method with your own imported method
                validation_error = validate_file(file)
                
                # Return the validation error as an HTTP response
                return HttpResponse(json.dumps(
                    {
                        'okay': validation_error is None,
                        'reason': str(validation_error),
                    }
                ))
            except ObjectDoesNotExist as e:
                raise Http404(str(e)) from e  
          ```
4. Add a new URL to the `urlpatterns` list to ensure that the system is able to effectively post the file to the server on User-provided file on User input
    * Navigate to the `rna-nanostructures/django_airavata/apps/api/urls.py` file
    * Append a new URL to the `urlpatterns` list using the following formatting:
        * `url(r'^my-custom-validator', views.file_validation),`
        * **NOTE:** Replace `my-custom-validator` with the name of the custom validator and replace `file_validation` with the name of the method implemented in Step 3.
5. Implement the custom `javascript` validation file created in Step 1.
    * Navigate to the file created in Step 1
    * Using the following template implement the respective class
        * ```javascript
          import FetchUtils from "../../utils/FetchUtils";
          export default class MyCustomValidator {
            constructor(config) {
                this.customErrorMessage = null;
                
                // Collect the alternative custom output message provided in the configurations
                if ("message" in config) {
                  this.customErrorMessage = config["message"];
                }
            }

            validate(value) {
                if (value === null || typeof value === "undefined") {
                  return 'The provided input must be a file.';
                }

                // TODO: Replace `my-custom-validator` with the value implemented as the url in Step 4
                return FetchUtils.get('/api/my-custom-validator', {
                  dataProductURI: value,
                }).then((response) => {
                  return response['reason']
                }).catch((error) => {
                  return error
                })
            }
          }
6. Now with this all of the setup complete to add the file validation: 
    * start the application and navigate to the settings screen and then to the application you wish to edit.
    * Once in the settings screen, select the application that you want to add validation to.
    * Now navigate to interface.
    * In the Input fields section make sure the input type is URI
    * For the validation add in the Advanced Input Field Modification Metadata section:
        * ```json
            {
                "editor": {
                    "validations": [
                        {
                            "type": "custom_validator"
                        }
                    ]
                }
            }
          ```
          **NOTE:** The "custom_validator" would change to be name given in the validatorFacotry
    * Click save at the bottem.
    * Now the validator should be added to that input of the application
