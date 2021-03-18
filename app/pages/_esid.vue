<template>
  <div>
    <Instructions
      v-if="showInstructions"
      @instructions-read="showInstructions = false"
    />
    <RankingForm
      v-else
      :es-id="esid"
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
  name: 'EsId',
  components: { RankingForm, Instructions },
  // eslint-disable-next-line require-await
  async asyncData({ params }) {
    const esid = params.esid // When calling /abc the esid will be "abc"
    return { esid }
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
    })
    // check if mturk params available
    if ('hitId' in this.$route.query) {
      this.assignmentId = this.$route.query.assignmentId
      this.hitId = this.$route.query.hitId
      this.workerId = this.$route.query.workerId
      // the URL to submit to is set in proxy config to prevent CORS issues
    }
  },
}
</script>

<style scoped></style>
