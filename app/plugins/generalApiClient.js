export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const generalApiClient = {
    heartbeat: async () => {
      let apiAlive
      try {
        const resp = await app.$axios.get('/api/heartbeat', jsonHeaderConfig)
        if (resp.status === 200) {
          apiAlive = resp.data
        } else {
          apiAlive = false
        }
      } catch (error) {
        window.console.error(error)
        apiAlive = false
      }
      return apiAlive
    },
  }

  // inject methods so that they can be called in any component or function with this.$generalApiClient.
  inject('generalApiClient', generalApiClient)
}
