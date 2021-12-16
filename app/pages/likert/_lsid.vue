<template>
  <div>
    <NotLoggedIn
      v-if="!mturkMode && (currentUser === null || currentUser === undefined)"
    />
    <LikertForm
      v-else
      :ls-id="lsId"
      :assignment-id="assignmentId"
      :worker-id="workerId"
      :hit-id="hitId"
    />
  </div>
</template>

<script>
import LikertForm from '../../components/LikertForm'
import NotLoggedIn from '../../components/NotLoggedIn'

export default {
  name: 'LsId',
  components: { NotLoggedIn, LikertForm },
  // eslint-disable-next-line require-await
  async asyncData({ params }) {
    const lsId = params.lsid // When calling /abc the lsid will be "abc"
    return { lsId }
  },
  data() {
    return {
      showInstructions: true,
      assignmentId: null,
      hitId: null,
      workerId: null,
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
