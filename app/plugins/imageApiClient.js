import { logger } from './logger'

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
          `${app.$config.ctxPath}api/image/${imgId}`,
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
    getUrls: async (imgIds) => {
      try {
        const resp = await app.$axios.post(
          `${app.$config.ctxPath}api/image/urls`,
          imgIds,
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
    getIds: async (imgUrls) => {
      try {
        const resp = await app.$axios.post(
          `${app.$config.ctxPath}api/image/ids`,
          imgUrls,
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

  // inject methods so that they can be called in any component or function with this.$imageApiClient.
  inject('imageApiClient', imageApiClient)
}
