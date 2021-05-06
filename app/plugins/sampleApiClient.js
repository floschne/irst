import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const sampleApiClient = {
    nextRankingSample: async () => {
      return await app.$axios
        .get(`${app.$config.ctxPath}api/ranking_sample/next`, jsonHeaderConfig)
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            return null
          }
        })
        .catch((error) => {
          logger('e', error)
          return null
        })
    },
    loadRankingSample: async (rsId) => {
      return await app.$axios
        .get(
          `${app.$config.ctxPath}api/ranking_sample/${rsId}`,
          jsonHeaderConfig
        )
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            return null
          }
        })
        .catch((error) => {
          logger('e', error)
          return null
        })
    },
    nextLikertSample: async () => {
      return await app.$axios
        .get(`${app.$config.ctxPath}api/likert_sample/next`, jsonHeaderConfig)
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            return null
          }
        })
        .catch((error) => {
          logger('e', error)
          return null
        })
    },
    loadLikertSample: async (lsId) => {
      return await app.$axios
        .get(
          `${app.$config.ctxPath}api/likert_sample/${lsId}`,
          jsonHeaderConfig
        )
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            return null
          }
        })
        .catch((error) => {
          logger('e', error)
          return null
        })
    },
  }

  // inject methods so that they can be called in any component or function with this.$sampleApiClient.
  inject('sampleApiClient', sampleApiClient)
}
