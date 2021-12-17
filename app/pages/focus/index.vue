<template>
  <div class="w-100">
    <NotLoggedIn
      v-if="!mturkMode && (currentUser === null || currentUser === undefined)"
    />
    <div v-else>
      <RatingWithFocusInstructions
        v-if="showInstructions"
        @rating-with-focus-instructions-read="showInstructions = false"
      />
      <RatingWithFocusForm v-else />
    </div>
  </div>
</template>

<script>
import RatingWithFocusForm from '../../components/RatingWithFocusForm'
import RatingWithFocusInstructions from '../../components/RatingWithFocusInstructions'
import NotLoggedIn from '../../components/NotLoggedIn'

export default {
  name: 'Index',
  components: { NotLoggedIn, RatingWithFocusForm, RatingWithFocusInstructions },
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
      localStorage.setItem('ratingWithFocusInstructionsRead', 'false')
    })
  },
}
</script>
