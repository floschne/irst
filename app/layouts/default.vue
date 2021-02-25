<template>
  <div class="vh-100">
    <AppHeader />
    <main class="container-fluid h-100" role="main" style="padding-top: 60px">
      <Nuxt />
    </main>
  </div>
</template>

<script>
import AppHeader from '~/components/AppHeader'
export default {
  components: { AppHeader },
}
</script>

<style>
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
