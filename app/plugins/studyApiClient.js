export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const studyApiClient = {
    getProgress: async () => {
      try {
        const resp = await app.$axios.get(
          '/api/study/progress',
          jsonHeaderConfig
        )
        if (resp.status === 200) {
          return resp.data
        } else {
          window.console.error(resp.status)
          return null
        }
      } catch (error) {
        window.console.error(error)
        return null
      }
    },
  }

  // inject methods so that they can be called in any component or function with this.$sampleApiClient.
  inject('studyApiClient', studyApiClient)
}
