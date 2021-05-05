<template>
  <b-container class="d-flex flex-row justify-content-center" fluid>
    <!-- Error Alert -->
    <b-alert variant="danger" :show="error && !success">
      Sorry, your Feedback was not submitted. Please try again!
    </b-alert>

    <!-- Success Alert -->
    <b-alert variant="success" :show="success && !error">
      Thanks! Your Feedback was submitted successfully! Feedback ID:
      {{ feedbackId }}
    </b-alert>
    <b-form
      v-if="!success && !error"
      class="w-100"
      @submit="onSubmit"
      @reset="onReset"
    >
      <b-form-row v-if="workerId !== ''" class="mb-1 align-items-center">
        <b-col sm="2">
          <label for="workerId">WorkerID:</label>
        </b-col>
        <b-col sm="10">
          <b-form-input
            id="workerId"
            v-model="submitWorkerId"
            name="workerId"
            type="text"
            readonly
            size="sm"
          ></b-form-input>
        </b-col>
      </b-form-row>

      <b-form-row class="mb-1">
        <b-form-textarea
          id="message"
          v-model="message"
          :state="isValidMessage"
          type="text"
          placeholder="Please enter your feedback here..."
          required
          rows="8"
        ></b-form-textarea>
        <b-form-invalid-feedback :state="isValidMessage">
          Please enter between 10 and 1000 characters!
        </b-form-invalid-feedback>
      </b-form-row>

      <b-form-row class="mb-1 mt-1">
        <b-button type="submit" variant="primary" class="w-50" size="sm">
          Submit
        </b-button>
        <b-button type="reset" variant="danger" class="w-50" size="sm">
          Reset
        </b-button>
      </b-form-row>

      <b-form-row v-if="workerId !== ''">
        <b-form-checkbox
          v-model="anonymous"
          name="show-next-time-checkbox"
          class="text-left"
          switch
        >
          Anonymous Feedback
        </b-form-checkbox>
      </b-form-row>
    </b-form>
  </b-container>
</template>

<script>
export default {
  name: 'FeedbackForm',
  props: {
    workerId: {
      type: String,
      default: '',
    },
    hitId: {
      type: String,
      default: '',
    },
    rsId: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      message: '',
      error: false,
      success: false,
      anonymous: false,
      feedbackId: null,
    }
  },
  computed: {
    submitWorkerId() {
      if (this.anonymous) return '************'
      else return this.workerId
    },
    isValidMessage() {
      return this.message.length >= 10 && this.message.length <= 1000
    },
  },
  methods: {
    async onSubmit(evt) {
      evt.preventDefault()
      const resp = await this.$feedbackApiClient.submitFeedback(
        this.rsId,
        this.message,
        this.submitWorkerId,
        this.hitId
      )
      if (resp !== null) {
        this.feedbackId = resp
        this.success = true
        this.error = false
      } else {
        this.success = false
        this.error = true
      }
    },
    onReset(evt) {
      evt.preventDefault()
      this.message = ''
      this.anonymous = false
      this.success = false
      this.error = false
      this.feedbackId = null
    },
  },
}
</script>

<style scoped></style>
