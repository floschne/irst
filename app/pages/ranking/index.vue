<template>
  <div class="w-100">
    <RankingInstructions
      v-if="showInstructions"
      @ranking-instructions-read="showInstructions = false"
    />
    <RankingForm v-else :min-num-ranks="$config.minNumRanks" />
  </div>
</template>

<script>
import RankingForm from '~/components/RankingForm'
import RankingInstructions from '~/components/RankingInstructions'

export default {
  name: 'Index',
  components: { RankingForm, RankingInstructions },
  data() {
    return {
      showInstructions: true,
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.current_user.currentUser
    },
    mturkMode() {
      return 'hitId' in this.$route.query
    },
  },
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
      localStorage.setItem('rankingInstructionsRead', 'false')
    })
  },
}
</script>
