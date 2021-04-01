<template>
  <div>
    <vue-good-table
      :columns="columns"
      :rows="rows"
      styleClass="vgt-table condensed bordered striped"
      :pagination-options="{
        enabled:true,
        mode:'records',
        perPage:'15',
      }"
    />
  </div>
</template>

<script>
import 'vue-good-table/dist/vue-good-table.css'
import { VueGoodTable } from 'vue-good-table';

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
          label: '#',
          field: 'name',
        },
        {
          label: 'Score',
          field: 'score',
        },
        {
          label: 'Design Sequence',
          field: 'sequence',
          width: '200px'
        },
        {
          label: 'Design Structure',
          field: 'structure',
        },
        {
          label: 'Motifs Uses',
          field: 'motifs',
        },
        {
          label: 'Opt Num',
          field: 'opt',
          width: '120px'
        },
        {
          label: 'Opt Seq',
          field: 'optSeq',
        },
        {
          label: 'Opt Score',
          field: 'optScore',
          width: '120px'
        },
        {
          label: 'Thermo Fluc Best Score',
          field: 'thermoBest',
          width: '220px'
        },
        {
          label: 'Hit Count',
          field: 'hit',
          width: '120px'
        },
      ],
      rows: [],
    }
  },
  watch: {
    viewData: {
      deep: true,
      handler() {
        for (let i = 1; i < this.viewData["csv"].length; i++) {
          let array = this.viewData["csv"][i].split(',');
          let row = {
            name:array[0],
            score:array[1],
            sequence:array[2],
            structure:array[3],
            motifs:array[4],
            opt:array[5],
            optSeq:array[6],
            optScore:array[7],
            thermoBest:array[8],
            hit:array[9]
          };
          this.rows.push(row);
        }
      }
    }
  },
};
</script>