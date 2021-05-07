<template>
  <div class="w-100">
    <RatingForm />
  </div>
</template>

<script>
import RatingForm from '~/components/RatingForm'

export default {
  name: 'Index',
  components: { RatingForm },
  data() {
    return {
      showInstructions: true,
    }
  },
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
      localStorage.setItem('instructionsRead', 'false')
    })
  },
}
</script>
