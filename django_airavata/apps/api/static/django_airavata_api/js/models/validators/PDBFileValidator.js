import FetchUtils from "../../utils/FetchUtils";
export default class PDBFileValidator {
  constructor(config) {
    this.customErrorMessage = null;
    
    if ("message" in config) {
      this.customErrorMessage = config["message"];
    }
  }

  validate(value) {
    if (value === null || typeof value === "undefined") {
      return 'The provided input must be a PDB file.';
    }

    return FetchUtils.get('/api/pdb-validator', {
      dataProductURI: value,
    }).then((response) => {
      return response['reason']
    }).catch((error) => {
      return error
    })
  }
}