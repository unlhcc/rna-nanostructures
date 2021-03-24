<template>
  <div>
    <vue-good-table
      :columns="columns"
      :rows="createRows"
      :pagination-options="{
        enabled:true,
        mode:'records',
        perPage:'15',
      }"
    />
  </div>
</template>

<script>
  export default {
    name: 'pdb-table-viewer',
    description: 'PDB Table Viewer',
    props: {
        viewData: {
          type: Object,
          required: true,
        },
    },
    data: {
      columns: createColumns(),
      rows: [],
    },
    computed: {
      generateTableData() {
        if (this.viewData["csv"]) {
          createRows();
        }
        return this.rows;
      }
    },
    methods: {
      createRows() {
        for (i = 1; i < this.viewData["csv"].length; i++) {
          let array = this.viewData["csv"][i].split(',');
          let row = {name:array[0], score:array[1], sequence:array[2], structure:array[3], motifs:array[4], opt:array[5], optSeq:array[6], optScore:array[7], thermoBest:array[8], hit:array[9]};
          this.rows.push(row);
        }
      },
      createColumns() {
        let columns = [
          {
            label: 'Design Number',
            field: 'name',
          },
          {
            label: 'Design Score',
            field: 'score',
          },
          {
            label: 'Design Sequence',
            field: 'sequence',
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
          },
          {
            label: 'Opt Seq',
            field: 'optSeq',
          },
          {
            label: 'Opt Score',
            field: 'optScore',
          },
          {
            label: 'Thermo Fluc Best Score',
            field: 'thermoBest',
          },
          {
            label: 'Hit Count',
            field: 'hit',
          },
        ]

        return columns;
      }
    }
  };
</script>