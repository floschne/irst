<template>
  <div class="w-100">
    <NotLoggedIn
      v-if="!mturkMode && (currentUser === null || currentUser === undefined)"
    />
    <LikertForm v-else />
  </div>
</template>

<script>
import LikertForm from '../../components/LikertForm'

export default {
  name: 'Index',
  components: { LikertForm },
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
