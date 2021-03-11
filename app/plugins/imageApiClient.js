import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const imageApiClient = {
    getUrls: async (imgIds, thumbnail = false) => {
      try {
        let u = `${app.$config.ctxPath}api/image/`
        if (thumbnail) u += 'thumbnails'
        else u += 'urls'
        const resp = await app.$axios.post(u, imgIds, jsonHeaderConfig)
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
