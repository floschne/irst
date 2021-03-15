import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  const userApiClient = {
    authenticate: async (userId, pwd) => {
      const userData = {
        id: userId,
        password: pwd,
      }
      return await app.$axios
        .post(
          `${app.$config.ctxPath}api/user/authenticate`,
          userData,
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
          if (error.request.status === 403) {
            logger('w', error.request.response)
            return JSON.parse(error.request.response)
          }
        })
    },
  }

  // inject methods so that they can be called in any component or function with this.$userApiClient.
  inject('userApiClient', userApiClient)
}
