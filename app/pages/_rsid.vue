<template>
  <div>
    <Instructions
      v-if="showInstructions"
      @instructions-read="showInstructions = false"
    />
    <RankingForm
      v-else
      :rs-id="rsId"
      :min-num-ranks="$config.minNumRanks"
      :assignment-id="assignmentId"
      :worker-id="workerId"
      :hit-id="hitId"
    />
  </div>
</template>

<script>
import RankingForm from '~/components/RankingForm'
import Instructions from '~/components/Instructions'

export default {
  name: 'RsId',
  components: { RankingForm, Instructions },
  // eslint-disable-next-line require-await
  async asyncData({ params }) {
    const rsid = params.rsid // When calling /abc the rsid will be "abc"
    return { rsid }
  },
  data() {
    return {
      showInstructions: true,
      assignmentId: null,
      hitId: null,
      workerId: null,
    }
  },
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
      localStorage.setItem('instructionsRead', 'false')
    })
    // check if mturk params available
    if ('hitId' in this.$route.query) {
      // the URL to submit to is set in proxy config to prevent CORS issues
      this.assignmentId = this.$route.query.assignmentId
      this.hitId = this.$route.query.hitId
      this.workerId = this.$route.query.workerId
    }
  },
}
</script>

<style scoped></style>
