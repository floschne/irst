<template>
  <b-container fluid>
    <!-- LOGIN FORM -->
    <LoginForm
      v-if="!loginSuccess"
      class="mt-5"
      @auth-success="loginSuccess = true"
    />
    <!-- Registration Success Jumbotron -->
    <b-jumbotron
      v-if="loginSuccess"
      class="rounded m-0"
      fluid
      bg-variant="success"
      text-variant="dark"
      :header="`Login successful! Welcome, ${currentUserName}!`"
      lead="You can now start using the app!"
    >
      <b-button to="/" variant="primary"> Start! </b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
import LoginForm from '~/components/LoginForm'
export default {
  name: 'Login',
  components: { LoginForm },
  data() {
    return {
      loginSuccess: false,
    }
  },
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
  methods: {},
}
</script>

<style scoped></style>
