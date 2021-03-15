<template>
  <b-container class="d-flex flex-row justify-content-center">
    <b-card
      v-if="errorMessage === ''"
      bg-variant="light"
      header="Authenticate"
      class="shadow shadow-lg"
    >
      <b-form v-if="show" @submit="onSubmit" @reset="onReset">
        <b-form-row class="mb-2">
          <b-form-input
            id="userID"
            v-model="userId"
            type="text"
            placeholder="Enter your user name!"
            required
          ></b-form-input>
        </b-form-row>

        <b-form-row class="mb-2">
          <b-form-input
            id="pwd"
            v-model="pwd"
            type="password"
            placeholder="Enter your password!"
            required
          ></b-form-input>
        </b-form-row>

        <b-form-row>
          <b-button type="submit" variant="primary" class="w-50" size="sm"
            >Submit</b-button
          >
          <b-button type="reset" variant="danger" class="w-50" size="sm"
            >Reset</b-button
          >
        </b-form-row>
      </b-form>
    </b-card>

    <!-- Error Jumbotron -->
    <b-jumbotron
      v-else
      class="rounded m-0"
      fluid
      bg-variant="danger"
      text-variant="dark"
      header="Could not authenticate!"
      :lead="errorMessage"
    >
      <b-button variant="primary" @click="onReset">Retry?!</b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
export default {
  name: 'LoginForm',
  emits: ['auth-success'],
  data() {
    return {
      pwd: '',
      userId: '',
      errorMessage: '',
      show: true,
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.authenticate(this.userId, this.pwd)
    },
    onReset(event) {
      event.preventDefault()
      this.pwd = ''
      this.userId = ''
      this.errorMessage = ''
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    },
    async authenticate(userId, pwd) {
      const resp = await this.$userApiClient.authenticate(userId, pwd)
      if ('jwt' in resp) {
        this.errorMessage = ''
        this.$emit('auth-success', resp.jwt)
      } else if ('detail' in resp) {
        this.errorMessage = resp.detail
      }
    },
  },
}
</script>

<style scoped></style>
