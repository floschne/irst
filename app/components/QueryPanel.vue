<template>
  <b-container class="p-0">
    <h3>
      Which images are best described by the following sentence? Please rank
      your Top 10!
    </h3>
    <b-form-textarea
      id="textarea-plaintext"
      plaintext
      rows="3"
      size="lg"
      max-rows="6"
      :value="query"
      trim
      class="p-1 border border-dark rounded"
    ></b-form-textarea>
  </b-container>
</template>

<script>
export default {
  name: 'QueryPanel',
  props: {
    query: {
      type: String,
      default: 'Loading Query...',
    },
  },
  data() {
    return {}
  },
}
</script>

<style scoped></style>
