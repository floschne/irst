<template>
  <b-jumbotron
    fluid
    header="Welcome to the Image Ranking User Study"
    lead="Please view the instructions below and make sure you understand what to do before you start!"
    class="rounded my-auto"
  >
    <b-button variant="primary" @click="onSubmit">
      Alright, let's start!
    </b-button>
  </b-jumbotron>
</template>

<script>
export default {
  name: 'Instructions',
  emits: ['instructions-read'],
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$emit('instructions-read')
    },
  },
}
</script>

<style scoped></style>
