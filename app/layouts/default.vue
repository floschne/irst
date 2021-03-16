<template>
  <div class="w-100 d-flex justify-content-center outer-container">
    <AppHeader />
    <main class="my-auto w-100" role="main">
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

<style lang="scss">
@import '~bootstrap/scss/functions';
@import '~bootstrap/scss/variables';
@import '~bootstrap/scss/mixins';

@include media-breakpoint-up(sm) {
  html {
    font-size: 0.75rem !important;
  }
  .app-header-text {
    font-size: $h4-font-size !important;
    font-family: $headings-font-family !important;
    font-weight: $headings-font-weight !important;
    line-height: $headings-line-height !important;
    margin-bottom: $headings-margin-bottom !important;
  }
  .drag-n-drop-text {
    font-size: $h3-font-size !important;
    font-family: $headings-font-family !important;
    font-weight: $headings-font-weight !important;
    line-height: $headings-line-height !important;
    margin-bottom: $headings-margin-bottom !important;
  }
}

@include media-breakpoint-up(md) {
  html {
    font-size: 0.8rem !important;
  }
  .app-header-text {
    font-size: $h3-font-size !important;
    font-family: $headings-font-family !important;
    font-weight: $headings-font-weight !important;
    line-height: $headings-line-height !important;
    margin-bottom: $headings-margin-bottom !important;
  }
  .drag-n-drop-text {
    font-size: $h2-font-size !important;
    font-family: $headings-font-family !important;
    font-weight: $headings-font-weight !important;
    line-height: $headings-line-height !important;
    margin-bottom: $headings-margin-bottom !important;
  }
}

@include media-breakpoint-up(lg) {
  html {
    font-size: 1rem !important;
  }
  .app-header-text {
    font-size: $h2-font-size !important;
    font-family: $headings-font-family !important;
    font-weight: $headings-font-weight !important;
    line-height: $headings-line-height !important;
    margin-bottom: $headings-margin-bottom !important;
  }
  .drag-n-drop-text {
    font-size: $h1-font-size !important;
    font-family: $headings-font-family !important;
    font-weight: $headings-font-weight !important;
    line-height: $headings-line-height !important;
    margin-bottom: $headings-margin-bottom !important;
  }
}

.outer-container {
  height: calc(100vh - 155px) !important;
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
