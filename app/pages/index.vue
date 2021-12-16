<template>
  <b-container fluid>
    <!-- LOGIN / REGISTER USER JUMBOTRON -->
    <NotLoggedIn v-if="currentUser === null || currentUser === undefined" />

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
      <b-button to="/focus" variant="primary">
        Image Rating With Focus User Study
      </b-button>
      <b-button to="/likert" variant="primary">
        Likert Questions User Study
      </b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
import NotLoggedIn from '../components/NotLoggedIn'

export default {
  name: 'Index',
  components: { NotLoggedIn },
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
