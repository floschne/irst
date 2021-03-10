<template>
  <RankingForm :num-ranks="$config.numRanks" />
</template>

<script>
import RankingForm from '~/components/RankingForm'

export default {
  name: 'Index',
  components: { RankingForm },
}
</script>
