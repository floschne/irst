<template>
  <div class="container-fluid">
    <AppHeader />
    <QueryPanel />
    <ImagesPanel class="mt-1" />
  </div>
</template>

<script>
import AppHeader from '~/components/AppHeader'
import QueryPanel from '~/components/QueryPanel'
import ImagesPanel from '~/components/ImagesPanel'

export default {
  components: { QueryPanel, ImagesPanel, AppHeader },
}
</script>
