<template>
  <div class="w-100">
    <RatingInstructions
      v-if="showInstructions"
      @rating-instructions-read="showInstructions = false"
    />
    <RatingForm v-else />
  </div>
</template>

<script>
import RatingForm from '~/components/RatingForm'
import RatingInstructions from '~/components/RatingInstructions'

export default {
  name: 'Index',
  components: { RatingForm, RatingInstructions },
  data() {
    return {
      showInstructions: true,
    }
  },
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
      localStorage.setItem('ratingInstructionsRead', 'false')
    })
  },
}
</script>
