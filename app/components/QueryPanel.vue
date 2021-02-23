<template>
  <b-container class="border border-dark rounded p-0">
    <b-form-textarea
      id="textarea-plaintext"
      plaintext
      rows="3"
      :value="text"
      trim
      class="p-1"
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
