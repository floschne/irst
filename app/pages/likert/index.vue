<template>
  <div class="w-100">
    <LikertForm />
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
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
      localStorage.setItem('rankingInstructionsRead', 'false')
    })
  },
}
</script>
