<template>
  <div>
    <b-dropdown id="visibility-dropdown" text="Column Visibility" class="m-md-2">
      <b-dropdown-item v-on:click="toggleScore">
        <b-form-checkbox :checked="!this.columns[1].hidden">
          Score Display
        </b-form-checkbox>
      </b-dropdown-item>
      <b-dropdown-item v-on:click="toggleOptSeq">
        <b-form-checkbox :checked="!this.columns[2].hidden">
          Opt Sequence
        </b-form-checkbox>
      </b-dropdown-item>
      <b-dropdown-item v-on:click="toggleDesignStructure">
        <b-form-checkbox :checked="!this.columns[3].hidden">
          Design Structure
        </b-form-checkbox>
      </b-dropdown-item>
      <b-dropdown-item v-on:click="toggleDesignSeq">
        <b-form-checkbox :checked="!this.columns[4].hidden">
          Design Sequence
        </b-form-checkbox>
      </b-dropdown-item>
      <b-dropdown-item v-on:click="toggleMotifs">
        <b-form-checkbox :checked="!this.columns[5].hidden">
          Motifs Used
        </b-form-checkbox>
      </b-dropdown-item>
    </b-dropdown>
    <p><em>Hover over a column header to read a brief description</em></p>
    <vue-good-table
      :columns="columns"
      :rows="rows"
      styleClass="vgt-table condensed bordered striped"
      :pagination-options="{
        enabled: true,
        mode: 'records',
        perPage: '15',
      }"
    />
  </div>
</template>

<script>
import "vue-good-table/dist/vue-good-table.css"
import { VueGoodTable } from "vue-good-table";

export default {
  name: "pdb-table-output-display",
  description: "PDB Table View",
  components: {
    VueGoodTable
  },
  props: {
    viewData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      columns: [
        {
          label: "#",
          field: "name",
          tooltip: "Design run number",
        },
        {
          label: "Score",
          field: "optScore",
          tooltip: "Accuracy to the target base pair: lower is better",
          width: "120px",
          hidden: false,
        },
        {
          label: "Opt Seq",
          field: "optSeq",
          tooltip: "Sequence after filling in the helical regions",
          hidden: false,
        },
        {
          label: "Design Structure",
          field: "structure",
          tooltip: "A representation of the design",
          hidden: false,
        },
        {
          label: "Design Sequence",
          field: "sequence",
          tooltip: "Unoptimized sequence with N's for helices",
          width: "200px",
          hidden: true,
        },
        {
          label: "Motifs Uses",
          field: "motifs",
          tooltip: "The motifs from the Motif library that were chosen",
          hidden: true,
        }
      ],
      rows: [],
    }
  },
  watch: {
    viewData: {
      deep: true,
      handler() {
        for (let i = 1; i < this.viewData["csv"].length; i++) {
          let array = this.viewData["csv"][i].split(",");

          // Motifs
          array[4] = array[4].replaceAll(";", "; ")
          // Design Sequence
          array[2] = this.splitInto(array[2], 33).join(" ")
          // Opt Sequence
          array[6] = this.splitInto(array[6], 33).join(" ")

          let row = {
            name: array[0],
            sequence: array[2],
            structure: array[3],
            motifs: array[4],
            optSeq: array[6],
            optScore: array[7],
          };
          this.rows.push(row);
        }
      }
    }
  },
  methods: {
    splitInto: function(str, len){
      var regex = new RegExp(".{1," + len + "}", "g");
      return str.match(regex);
    },
    toggleScore: function(){
      this.$set(this.columns[1], "hidden", !this.columns[1].hidden);
    },
    toggleOptSeq: function(){
      this.$set(this.columns[2], "hidden", !this.columns[2].hidden);
    },
    toggleDesignStructure: function(){
      this.$set(this.columns[3], "hidden", !this.columns[3].hidden);
    },
    toggleDesignSeq: function(){
      this.$set(this.columns[4], "hidden", !this.columns[4].hidden);
    },
    toggleMotifs: function(){
      this.$set(this.columns[5], "hidden", !this.columns[5].hidden);
    },
  }
};
</script>
