<template>
  <div class="container-fluid">
    <QueryPanel />
    <ImagesPanel />
    <RankingForm class="mt-3" />
  </div>
</template>

<script>
import QueryPanel from '~/components/QueryPanel'
import ImagesPanel from '~/components/ImagesPanel'
import RankingForm from '~/components/RankingForm'

export default {
  components: { QueryPanel, ImagesPanel, RankingForm },
}
</script>
