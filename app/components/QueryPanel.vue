<template>
  <b-container class="p-0">
    <h3>
      Which images are best described by the caption? Please rank your Top
      {{ numRanks }} !
    </h3>
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
    numRanks: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {}
  },
}
</script>

<style scoped></style>
