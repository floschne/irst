<template>
  <div>
    <RatingInstructions
      v-if="showInstructions"
      @rating-instructions-read="showInstructions = false"
    />
    <RatingForm
      v-else
      :rs-id="rsId"
      :assignment-id="assignmentId"
      :worker-id="workerId"
      :hit-id="hitId"
    />
  </div>
</template>

<script>
import RatingForm from '~/components/RatingForm'
import RatingInstructions from '~/components/RatingInstructions'

export default {
  name: 'RsId',
  components: { RatingForm, RatingInstructions },
  // eslint-disable-next-line require-await
  async asyncData({ params }) {
    const rsId = params.rsid // When calling /abc the rsId will be "abc"
    return { rsId }
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
      localStorage.setItem('ratingInstructionsRead', 'false')
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
