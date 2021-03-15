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
      let u = `${app.$config.ctxPath}api/image/`
      if (thumbnail) u += 'thumbnails'
      else u += 'urls'
      return await app.$axios
        .post(u, imgIds, jsonHeaderConfig)
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
    getIds: async (imgUrls) => {
      return await app.$axios
        .post(`${app.$config.ctxPath}api/image/ids`, imgUrls, jsonHeaderConfig)
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

  // inject methods so that they can be called in any component or function with this.$imageApiClient.
  inject('imageApiClient', imageApiClient)
}
