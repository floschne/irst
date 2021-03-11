<template>
  <div>
    <b-button
      size="sm"
      pill
      :variant="heartbeat ? 'success' : 'danger'"
      type="button"
      style="width: 145px"
      @click="checkHeartbeat"
    >
      API Status:
      <span v-if="heartbeat">alive</span>
      <span v-else>dead<b-icon-arrow-repeat /></span>
    </b-button>
  </div>
</template>

<script>
export default {
  name: 'HeartbeatCheckButton',
  emits: ['api-dead'],
  data() {
    return {
      heartbeat: Boolean(false),
    }
  },
  created() {
    this.checkHeartbeat()
  },
  methods: {
    async checkHeartbeat(evt) {
      if (evt !== undefined) {
        evt.preventDefault()
      }
      this.heartbeat = await this.$generalApiClient.heartbeat()
    },
  },
}
</script>

<style scoped></style>
