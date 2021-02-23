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
          apiAlive = resp.data.value
        } else {
          apiAlive = false
        }
      } catch (error) {
        console.error(error)
        apiAlive = false
      }
      console.log(`API Heartbeat: ${JSON.stringify(apiAlive)}`)
      return apiAlive
    },
  }

  // inject methods so that they can be called in any component or function with this.$generalApiClient.
  inject('generalApiClient', generalApiClient)
}
