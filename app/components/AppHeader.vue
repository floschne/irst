<template>
  <header>
    <b-navbar toggleable="md" type="dark" variant="dark" fixed="top">
      <b-navbar-brand to="/">
        Codebook Automation WebApp
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" />

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/datasets">
            Datasets
          </b-nav-item>
          <b-nav-item to="/training">
            Training
          </b-nav-item>
          <b-nav-item to="/models">
            Models
          </b-nav-item>
          <b-nav-item to="/prediction">
            Prediction
          </b-nav-item>
          <b-nav-item to="/docs">
            Docs
          </b-nav-item>
        </b-navbar-nav>

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
  components: { HeartbeatCheckButton }
}
</script>

<style scoped>

</style>
