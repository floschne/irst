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

      <b-navbar-nav>
        <b-nav-item to="/">
          <b-icon
            v-b-tooltip.hover.bottom="'Home'"
            font-scale="1.5"
            icon="house-fill"
          />
        </b-nav-item>
        <b-nav-item to="/profile">
          <b-icon
            v-b-tooltip.hover.bottom="'Profile'"
            font-scale="1.5"
            icon="person-lines-fill"
          />
        </b-nav-item>
        <b-nav-item>
          <b-icon
            v-b-tooltip.hover.bottom="'Help'"
            font-scale="1.5"
            icon="question-circle"
            @click="helpRequested"
          />
        </b-nav-item>
      </b-navbar-nav>

      <b-nav-text
        class="text-warning badge badge-success"
        v-html="currentUserName"
      >
      </b-nav-text>

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
  computed: {
    currentUser() {
      return this.$store.state.current_user.currentUser
    },
    currentUserName() {
      return this.currentUser === null
        ? ''
        : JSON.stringify(this.currentUser.userId).replaceAll('"', '')
    },
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
