export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const resultApiClient = {
    submitResult: async (esId, rankingData) => {
      const result = {
        es_id: esId,
        ranking: rankingData,
      }
      try {
        const resp = await app.$axios.put(
          '/api/result/submit',
          result,
          jsonHeaderConfig
        )
        if (resp.status === 200) {
          window.console.log(resp.data)
          return true
        } else {
          window.console.error(resp.status)
          return false
        }
      } catch (error) {
        window.console.error(error)
        return false
      }
    },
  }

  // inject methods so that they can be called in any component or function with this.$resultApiClient.
  inject('resultApiClient', resultApiClient)
}
