<template>
  <RankingForm :es-id="esid" />
</template>

<script>
import RankingForm from '~/components/RankingForm'

export default {
  name: 'EsId',
  components: { RankingForm },

  // eslint-disable-next-line require-await
  async asyncData({ params }) {
    const esid = params.esid // When calling /abc the slug will be "abc"
    return { esid }
  },
}
</script>

<style scoped></style>
