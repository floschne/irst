<template>
  <div>
    <Instructions
      v-if="showInstructions"
      @instructions-read="showInstructions = false"
    />
    <RankingForm v-else :es-id="esid" :num-ranks="$config.numRanks" />
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
    }
  },
  created() {
    this.$nuxt.$on('help-requested', () => {
      this.showInstructions = true
    })
  },
}
</script>

<style scoped></style>
