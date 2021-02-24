<template>
  <div class="container-fluid">
    <AppHeader />
    <QueryPanel />
    <RankingForm class="mt-1" />
  </div>
</template>

<script>
import AppHeader from '~/components/AppHeader'
import QueryPanel from '~/components/QueryPanel'
import RankingForm from '~/components/RankingForm'

export default {
  components: { QueryPanel, RankingForm, AppHeader },
}
</script>
