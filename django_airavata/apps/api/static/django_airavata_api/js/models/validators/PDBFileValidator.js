export default class PDBFileValidator {
    constructor(config) {
      this.file = config["value"];
      if ("message" in config) {
        this.customErrorMessage = config["message"];
      }
    }
  
    validate(value) {
      if (value === null || typeof value === "undefined") {
        return null;
      }
      if (typeof value !== File) {
          return "The provided input must be a file";
      } else if (pdb) {//placeholder
          return this.customErrorMessage;
      }
      //run validation then get the returned values if NONE then return null else return error
      
      // POST DataProductURI here

      // GET Response from PDB Validator script

      // Return response
      return null;      
    }
  
    getErrorMessage() {
      if (this.customErrorMessage) {
        return this.customErrorMessage;
      } else {
        return "The file must be a PDB";
      }
    }
  }