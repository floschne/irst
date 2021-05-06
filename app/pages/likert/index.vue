<template>
  <div class="w-100">
    <LikertScaleForm />
  </div>
</template>

<script>
import LikertScaleForm from '../../components/LikertScaleForm'

export default {
  name: 'Index',
  components: { LikertScaleForm },
  data() {
    return {
      showInstructions: true,
    }
  },
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
      localStorage.setItem('instructionsRead', 'false')
    })
  },
}
</script>
