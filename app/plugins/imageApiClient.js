export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const imageApiClient = {
    getUrl: async (imgId) => {
      try {
        const resp = await app.$axios.get(
          `/api/image/${imgId}`,
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
    getUrls: async (imgIds) => {
      try {
        const resp = await app.$axios.post(
          '/api/image/urls',
          imgIds,
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

  // inject methods so that they can be called in any component or function with this.$imageApiClient.
  inject('imageApiClient', imageApiClient)
}
