<template>
  <b-container class="border border-dark rounded">
    <b-form-textarea
      id="textarea-plaintext"
      plaintext
      rows="3"
      :value="text"
      trim
    ></b-form-textarea>
  </b-container>
</template>

<script>
export default {
  name: 'QueryPanel',
  data() {
    return {
      text:
        "This is some text.\nIt is read only and doesn't look like an input.",
    }
  },
}
</script>

<style scoped></style>
