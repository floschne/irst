import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const generalApiClient = {
    heartbeat: async () => {
      return await app.$axios
        .get(`${app.$config.ctxPath}api/heartbeat`, jsonHeaderConfig)
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            return false
          }
        })
        .catch((error) => {
          logger('e', error)
          return false
        })
    },
  }

  // inject methods so that they can be called in any component or function with this.$generalApiClient.
  inject('generalApiClient', generalApiClient)
}
