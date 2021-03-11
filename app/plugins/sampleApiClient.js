import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const sampleApiClient = {
    nextSample: async () => {
      try {
        const resp = await app.$axios.get(
          `${app.$config.ctxPath}api/sample/next`,
          jsonHeaderConfig
        )
        if (resp.status === 200) {
          return resp.data
        } else {
          logger('e', resp)
          return null
        }
      } catch (error) {
        logger('e', error)
        return null
      }
    },
    load: async (esId) => {
      try {
        const resp = await app.$axios.get(
          `${app.$config.ctxPath}api/sample/${esId}`,
          jsonHeaderConfig
        )
        if (resp.status === 200) {
          return resp.data
        } else {
          logger('e', resp)
          return null
        }
      } catch (error) {
        logger('e', error)
        return null
      }
    },
  }

  // inject methods so that they can be called in any component or function with this.$sampleApiClient.
  inject('sampleApiClient', sampleApiClient)
}
