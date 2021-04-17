import FetchUtils from "../../utils/FetchUtils";

export default class PDBFileValidator {
  constructor(config) {
    if ("message" in config) {
      this.customErrorMessage = config["message"];
    }
  }

  validate(value) {
    if (value === null || typeof value === "undefined") {
      return null;
    }
    FetchUtils.get('/api/pdb-validator', {
      dataProductURI: value,
    }).then((response) => {
      console.log('Response from PDB Validator:', response); // TODO
    }).catch((error) => {
      console.error('Error communicating with PDB Validator:', error); // TODO
    });
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