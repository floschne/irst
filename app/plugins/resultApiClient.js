import { logger } from './logger'

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
      logger('i', result)
      try {
        const resp = await app.$axios.put(
          `${app.$config.ctxPath}api/result/submit`,
          result,
          jsonHeaderConfig
        )
        if (resp.status === 200) {
          return true
        } else {
          logger('e', resp)
          return false
        }
      } catch (error) {
        logger('e', error)
        return false
      }
    },
  }

  // inject methods so that they can be called in any component or function with this.$resultApiClient.
  inject('resultApiClient', resultApiClient)
}
