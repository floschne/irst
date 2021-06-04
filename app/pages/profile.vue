<template>
  <b-container fluid>
    <!-- LOGIN / REGISTER USER JUMBOTRON -->
    <b-jumbotron
      v-if="currentUser === null"
      header="Welcome to the Image Ranking Study Tool!"
      lead="Please login or register to start using the tool."
    >
      <b-button to="/login" variant="primary"> Login </b-button>
      <b-button to="/register" variant="success"> Register </b-button>
    </b-jumbotron>

    <!-- LOGOUT USER JUMBOTRON -->
    <b-jumbotron
      v-if="currentUser !== null"
      :header="`Welcome, ${currentUserName}!`"
      lead="Do you want to logout?"
    >
      <b-button variant="danger" @click="clearCurrentUser"> Logout </b-button>
      <b-button variant="primary" to="/"> Home </b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Profile',
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
  methods: {
    ...mapMutations({
      clearCurrentUser: 'current_user/clearCurrentUser',
    }),
  },
}
</script>

<style scoped></style>
