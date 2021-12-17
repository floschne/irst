<template>
  <div>
    <NotLoggedIn
      v-if="!mturkMode && (currentUser === null || currentUser === undefined)"
    />
    <div v-else>
      <RatingWithFocusInstructions
        v-if="showInstructions"
        @rating-with-focus-instructions-read="showInstructions = false"
      />
      <RatingWithFocusForm
        v-else
        :rs-id="rsId"
        :assignment-id="assignmentId"
        :worker-id="workerId"
        :hit-id="hitId"
      />
    </div>
  </div>
</template>

<script>
import RatingWithFocusForm from '../../components/RatingWithFocusForm'
import RatingWithFocusInstructions from '../../components/RatingWithFocusInstructions'
import NotLoggedIn from '../../components/NotLoggedIn'

export default {
  name: 'RsId',
  components: { NotLoggedIn, RatingWithFocusForm, RatingWithFocusInstructions },
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
      localStorage.setItem('ratingWithFocusInstructionsRead', 'false')
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
