<template>
  <div>
    <p>Hello world</p>
    <vue-good-table
      :columns="columns"
      :rows="rows"
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
      data: {
        columns: [
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
        ],
        rows: [],
      }
    },
    watch: {
      generateTableRows: {
        deep: true,
        handler: function () {
          for (let i = 1; i < this.viewData["csv"].length; i++) {
            let array = this.viewData["csv"][i].split(',');
            let row = {name:array[0], score:array[1], sequence:array[2], structure:array[3], motifs:array[4], opt:array[5], optSeq:array[6], optScore:array[7], thermoBest:array[8], hit:array[9]};
            this.rows.push(row);
          }
        }
      }
    },
    computed: {
      generateTableData() {
        if (this.viewData["csv"]) {
          // this.createRows();
          // for (let i = 1; i < this.viewData["csv"].length; i++) {
          //   let array = this.viewData["csv"][i].split(',');
          //   let row = {name:array[0], score:array[1], sequence:array[2], structure:array[3], motifs:array[4], opt:array[5], optSeq:array[6], optScore:array[7], thermoBest:array[8], hit:array[9]};
          //   this.rows.push(row);
          // }
          
        }
        return null;
      }
    },
    // methods: {
    //   createRows() {
    //     for (let i = 1; i < this.viewData["csv"].length; i++) {
    //       let array = this.viewData["csv"][i].split(',');
    //       let row = {name:array[0], score:array[1], sequence:array[2], structure:array[3], motifs:array[4], opt:array[5], optSeq:array[6], optScore:array[7], thermoBest:array[8], hit:array[9]};
    //       this.rows.push(row);
    //     }
    //   },
    //   createColumns() {
    //     let columns = [
    //       {
    //         label: 'Design Number',
    //         field: 'name',
    //       },
    //       {
    //         label: 'Design Score',
    //         field: 'score',
    //       },
    //       {
    //         label: 'Design Sequence',
    //         field: 'sequence',
    //       },
    //       {
    //         label: 'Design Structure',
    //         field: 'structure',
    //       },
    //       {
    //         label: 'Motifs Uses',
    //         field: 'motifs',
    //       },
    //       {
    //         label: 'Opt Num',
    //         field: 'opt',
    //       },
    //       {
    //         label: 'Opt Seq',
    //         field: 'optSeq',
    //       },
    //       {
    //         label: 'Opt Score',
    //         field: 'optScore',
    //       },
    //       {
    //         label: 'Thermo Fluc Best Score',
    //         field: 'thermoBest',
    //       },
    //       {
    //         label: 'Hit Count',
    //         field: 'hit',
    //       },
    //     ]

    //     return columns;
    //   }
    // }
  };
</script>