<template>
  <b-jumbotron
    header="Welcome to the Image Ranking Study Tool!"
    lead="Please login or register to start using the tool."
  >
    <b-button to="/login" variant="primary"> Login </b-button>
    <b-button to="/register" variant="success"> Register </b-button>
  </b-jumbotron>
</template>

<script>
export default {
  name: 'NotLoggedIn',
}
</script>

<style scoped></style>
