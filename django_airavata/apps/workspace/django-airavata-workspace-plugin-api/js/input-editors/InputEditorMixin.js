// InputEditorMixin: mixin for experiment InputEditors, provides basic v-model
// and validation functionality and defines the basic props interface
// (experimentInput and id).

/* eslint-disable no-console */ //TODO
import { models } from "django-airavata-api";
export default {
  props: {
    value: {
      type: String,
    },
    experimentInput: {
      type: models.InputDataObjectType,
      required: true,
    },
    experiment: {
      type: models.Experiment,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      data: this.value,
      inputHasBegun: false,
    };
  },
  asyncComputed: {
    // POTENTIAL SOLUTION
    // validationResults: {
    //   get() {
    //     return this.experimentInput.validate(this.data)
    //   },
    //   default: 'Validating Input...'
    // }
    validationResults: {      
      get () {
        let results = this.experimentInput.validate(this.data);
        return {
          "value": [new Promise(resolve => resolve(results.value[0]))]
        };
      },
      default () {
        return {
          "value": ["Validating Input..."]
        }
      }
      // return this.experimentInput.validate(this.data);
    },
    // validationResults: function () {      
    //   return new Promise(resolve => resolve(this.experimentInput.validate(this.data)));

    //   // return this.experimentInput.validate(this.data);
    // },
    validationMessages: function () {
      console.log('ValidationResults = ', this.validationResults["value"]); // TODO
      console.log('ValidationResults return: ', "value" in this.validationResults ? this.validationResults["value"] : [])
      return "value" in this.validationResults
        ? this.validationResults["value"]
        : [];
    },
    valid: function () {
      console.log('ValidationMessage = ', this.validationMessages); // TODO
      if (this.validationMessages)
        return this.validationMessages.length === 0;
      else
        return false;
      
      // return true;
      // return this.validationMessages.length === 0;
    },
    componentValidState: function () {
      if (this.inputHasBegun) {
        return this.valid ? "valid" : "invalid";
      } else {
        return null;
      }
    },
    editorConfig: function () {
      return this.experimentInput.editorConfig;
    },
  },
  methods: {
    valueChanged: function () {
      this.inputHasBegun = true;
      this.$emit("input", this.data);
    },
    checkValidation: function () {
      if (this.valid) {
        this.$emit("valid");
      } else {
        this.$emit("invalid", this.validationMessages);
      }
    },
  },
  created: function () {
    this.checkValidation();
  },
  watch: {
    value(newValue) {
      this.data = newValue;
    },
    valid() {
      this.checkValidation();
    },
  },
};
