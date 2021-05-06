<template>
  <div>
    <LikertForm
      :ls-id="lsId"
      :assignment-id="assignmentId"
      :worker-id="workerId"
      :hit-id="hitId"
    />
  </div>
</template>

<script>
import LikertForm from '../../components/LikertForm'

export default {
  name: 'LsId',
  components: { LikertForm },
  // eslint-disable-next-line require-await
  async asyncData({ params }) {
    const lsid = params.lsid // When calling /abc the lsid will be "abc"
    return { lsid }
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
