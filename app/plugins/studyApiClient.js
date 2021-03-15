import { logger } from './logger'

export default ({ app, axios }, inject) => {
  // define the methods
  const studyApiClient = {
    getProgress: async (jwt) => {
      const authJsonHeaderConfig = {
        headers: {
          Accept: 'application/json',
          Authorization: 'Bearer ' + jwt,
        },
      }
      return await app.$axios
        .get(`${app.$config.ctxPath}api/study/progress`, authJsonHeaderConfig)
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            return null
          }
        })
        .catch((error) => {
          if (error.request.status === 403) {
            logger('w', error.request.response)
            return JSON.parse(error.request.response)
          }
        })
    },
  }

  // inject methods so that they can be called in any component or function with this.$studyApiClient.
  inject('studyApiClient', studyApiClient)
}
