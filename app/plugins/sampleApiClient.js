import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  async function nextSample(type) {
    return await app.$axios
      .get(`${app.$config.ctxPath}api/${type}_sample/next`, jsonHeaderConfig)
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
  }

  async function loadSample(type, sampleId) {
    return await app.$axios
      .get(
        `${app.$config.ctxPath}api/${type}_sample/${sampleId}`,
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
  }

  // define the methods
  const sampleApiClient = {
    nextRankingSample: async () => {
      return await nextSample('ranking')
    },
    loadRankingSample: async (rsId) => {
      return await loadSample('ranking', rsId)
    },
    nextLikertSample: async () => {
      return await nextSample('likert')
    },
    loadLikertSample: async (lsId) => {
      return await loadSample('likert', lsId)
    },
    nextRatingSample: async () => {
      return await nextSample('rating')
    },
    loadRatingSample: async (lsId) => {
      return await loadSample('rating', lsId)
    },
    nextRatingWithFocusSample: async () => {
      return await nextSample('rating_with_focus')
    },
    loadRatingWithFocusSample: async (lsId) => {
      return await loadSample('rating_with_focus', lsId)
    },
  }

  // inject methods so that they can be called in any component or function with this.$sampleApiClient.
  inject('sampleApiClient', sampleApiClient)
}
