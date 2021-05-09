<template>
  <header>
    <b-navbar
      toggleable="sm"
      type="dark"
      variant="dark"
      fixed="top"
      class="pt-0 pb-0"
    >
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-navbar-brand @click="helpRequested">
        <b-icon
          v-b-tooltip.hover.bottom="'Help'"
          font-scale="1.5"
          icon="question-circle"
        />
      </b-navbar-brand>

      <b-nav-text
        class="w-100 text-center p-0 m-0 text-warning"
        style="font-size: 2vw"
        v-html="headerText"
      >
      </b-nav-text>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <HeartbeatCheckButton />
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </header>
</template>

<script>
import HeartbeatCheckButton from '~/components/HeartbeatCheckButton'

export default {
  name: 'AppHeader',
  components: { HeartbeatCheckButton },
  emits: ['help-requested'],
  data() {
    return {
      headerText: 'Welcome!',
    }
  },
  created() {
    this.$nuxt.$on('set-app-header-text', (headerText) => {
      this.headerText = headerText
    })
  },
  methods: {
    helpRequested() {
      this.$nuxt.$emit('help-requested')
    },
  },
}
</script>

<style scoped></style>
