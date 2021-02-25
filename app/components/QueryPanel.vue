<template>
  <b-container class="border border-dark rounded p-0">
    <b-form-textarea
      id="textarea-plaintext"
      plaintext
      rows="3"
      size="lg"
      max-rows="6"
      :value="query"
      trim
      class="p-1"
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
