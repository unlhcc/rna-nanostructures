<template>
  <div>
    <vue-good-table
      :columns="columns"
      :rows="rows"/>
  </div>
</template>

<script>
export default {
  name: 'my-component',
  data(){
    return {
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
      rows: [
        // TODO
        // { id:1, name:"John", age: 20, createdAt: '',score: 0.03343 },
        // { id:2, name:"Jane", age: 24, createdAt: '2011-10-31', score: 0.03343 },
        // { id:3, name:"Susan", age: 16, createdAt: '2011-10-30', score: 0.03343 },
        // { id:4, name:"Chris", age: 55, createdAt: '2011-10-11', score: 0.03343 },
        // { id:5, name:"Dan", age: 40, createdAt: '2011-10-21', score: 0.03343 },
        // { id:6, name:"John", age: 20, createdAt: '2011-10-31', score: 0.03343 },
      ],
    };
  },
};
</script>

