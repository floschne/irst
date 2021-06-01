<template>
  <b-container class="d-flex flex-row justify-content-center">
    <b-card
      v-if="errorMessage === ''"
      bg-variant="light"
      header="Register"
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
          <b-button type="submit" variant="primary" class="w-50" size="sm">
            Submit
          </b-button>
          <b-button type="reset" variant="danger" class="w-50" size="sm">
            Reset
          </b-button>
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
      :header="`Could not register user ${userId}!`"
      :lead="errorMessage"
    >
      <b-button variant="primary" @click="onReset">Retry?!</b-button>
    </b-jumbotron>
  </b-container>
</template>

<script>
export default {
  name: 'RegistrationForm',
  emits: ['registration-success'],
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
      this.register(this.userId, this.pwd)
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
    async register(userId, pwd) {
      const resp = await this.$userApiClient.register(userId, pwd)
      if (resp) {
        this.errorMessage = ''
        this.$emit('registration-success')
      } else if ('detail' in resp) {
        this.errorMessage = resp.detail
      }
    },
  },
}
</script>

<style scoped></style>
