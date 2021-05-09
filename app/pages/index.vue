<template>
  <b-container fluid>
    <b-jumbotron
      header="Welcome to the Image Ranking Study Tool"
      lead="Start a study by clicking one of the buttons"
    >
      <b-button to="/ranking" variant="primary">
        Image Ranking User Study
      </b-button>
      <b-button to="/rating" variant="primary">
        Image Rating User Study
      </b-button>
      <b-button to="/likert" variant="primary">
        Image Likert Questions User Study
      </b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
export default {
  name: 'Index',
}
</script>

<style scoped></style>
