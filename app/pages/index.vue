<template>
  <b-container fluid>
    <!-- LOGIN / REGISTER USER JUMBOTRON -->
    <b-jumbotron
      v-if="currentUser === null || currentUser === undefined"
      header="Welcome to the Image Ranking Study Tool!"
      lead="Please login or register to start using the tool."
    >
      <b-button to="/login" variant="primary"> Login </b-button>
      <b-button to="/register" variant="success"> Register </b-button>
    </b-jumbotron>

    <!-- WELCOME USER JUMBOTRON -->
    <b-jumbotron
      v-if="currentUser !== null && currentUser !== undefined"
      :header="`Welcome to the Image Ranking Study Tool, ${currentUserName}!`"
      lead="Start a study by clicking one of the buttons"
    >
      <b-button to="/ranking" variant="primary">
        Image Ranking User Study
      </b-button>
      <b-button to="/rating" variant="primary">
        Image Rating User Study
      </b-button>
      <b-button to="/likert" variant="primary">
        Likert Questions User Study
      </b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
export default {
  name: 'Index',
  computed: {
    currentUser() {
      return this.$store.state.current_user.currentUser
    },
    currentUserName() {
      return this.currentUser === null
        ? ''
        : JSON.stringify(this.currentUser.userId).replaceAll('"', '')
    },
  },
}
</script>

<style scoped></style>
