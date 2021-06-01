<template>
  <b-container fluid>
    <!-- REGISTRATION FORM -->
    <RegistrationForm
      v-if="!registrationSuccess"
      class="mt-5"
      @registration-success="registrationSuccess = true"
    />

    <!-- Registration Success Jumbotron -->
    <b-jumbotron
      v-if="registrationSuccess"
      class="rounded m-0"
      fluid
      bg-variant="success"
      text-variant="dark"
      header="Registration successful!"
      lead="You can now login with your credentials."
    >
      <b-button to="/login" variant="primary"> Login </b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
import RegistrationForm from '~/components/RegistrationForm'
export default {
  name: 'Register',
  components: { RegistrationForm },
  data() {
    return {
      registrationSuccess: false,
    }
  },
}
</script>

<style scoped></style>
