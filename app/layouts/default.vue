<template>
  <div class="w-100 d-flex justify-content-center outer-container">
    <AppHeader />
    <main class="my-auto" role="main">
      <Nuxt />
    </main>
  </div>
</template>

<script>
import AppHeader from '~/components/AppHeader'
export default {
  components: { AppHeader },
  data() {
    return {
      rankingFooterSize: null,
    }
  },
}
</script>

<style>
.outer-container {
  height: calc(100vh - 160px) !important;
}

html {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}
</style>
