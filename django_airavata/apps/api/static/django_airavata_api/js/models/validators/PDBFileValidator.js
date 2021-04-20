/* eslint-disable no-console */

import FetchUtils from "../../utils/FetchUtils";
export default class PDBFileValidator {
  constructor(config) {
    this.customErrorMessage = null;
    
    if ("message" in config) {
      this.customErrorMessage = config["message"];
    }
  }

  async validate(value) {
    // console.log("Running PDB Validator")
    if (value === null || typeof value === "undefined") {
      return 'The provided input must be a PDB file';
    }

    return FetchUtils.get('/api/pdb-validator', {
      dataProductURI: value,
    }).then((response) => {
      // console.log('Response from PDB Validator:', response); // TODO
      return response['reason']
      //return response
      //this.customErrorMessage = response;
    }).catch((error) => {
      // eslint-disable-next-line no-console
      // console.error('Error communicating with PDB Validator:', error); // TODO
      // this.customErrorMessage = 'Error communicating with the PDB Validator';
      return error
    })
  }

  getErrorMessage() {
    if (this.customErrorMessage) {
      return this.customErrorMessage;
    } else {
      return "An error occurred while validating the PDB file.";
    }
  }
}