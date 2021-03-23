<template>
  <div class="w-100">
    <Instructions
      v-if="showInstructions"
      @instructions-read="showInstructions = false"
    />
    <RankingForm v-else :min-num-ranks="$config.minNumRanks" />
  </div>
</template>

<script>
import RankingForm from '~/components/RankingForm'
import Instructions from '~/components/Instructions'

export default {
  name: 'Index',
  components: { RankingForm, Instructions },
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
