<template>
  <header>
    <b-navbar toggleable="sm" type="dark" variant="dark" fixed="top">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-navbar-brand>Help</b-navbar-brand>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <HeartbeatCheckButton />
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </header>
</template>

<script>
import HeartbeatCheckButton from '@/components/HeartbeatCheckButton'

export default {
  name: 'AppHeader',
  components: { HeartbeatCheckButton },
  props: {
    numRanks: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      numRankedImages: 0,
    }
  },
}
</script>

<style scoped></style>
