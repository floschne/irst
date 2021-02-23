<template>
  <div class="container-fluid">
    <QueryPanel />
    <RankingForm class="mt-1" />
  </div>
</template>

<script>
import QueryPanel from '~/components/QueryPanel'
import RankingForm from '~/components/RankingForm'

export default {
  components: { QueryPanel, RankingForm },
}
</script>
