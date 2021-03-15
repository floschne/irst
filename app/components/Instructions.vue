<template>
  <b-jumbotron
    fluid
    header="Welcome!"
    lead="Please watch the instructions video and make sure you know what to do before you start!"
    class="rounded my-auto"
  >
    <div class="text-center">
      <iframe
        width="800"
        height="450"
        src="https://www.youtube-nocookie.com/embed/ErMXs3ydaqE?controls=0&vq=hd720"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>

      <b-button block variant="primary" @click="onSubmit">
        Alright, let's start!
      </b-button>
    </div>
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
