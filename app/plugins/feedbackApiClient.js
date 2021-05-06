import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const feedbackApiClient = {
    submitFeedback: async (sampleId, msg, workerId = '', hitId = '') => {
      const feedback = {
        sample_id: sampleId,
        message: msg,
        worker_id: workerId,
        hit_id: hitId,
      }
      return await app.$axios
        .put(
          `${app.$config.ctxPath}api/feedback/submit`,
          feedback,
          jsonHeaderConfig
        )
        .then((resp) => {
          if (resp.status === 200) {
            return resp.data
          } else {
            logger('e', resp)
            return null
          }
        })
        .catch((error) => {
          logger('e', error)
          return null
        })
    },
  }

  // inject methods so that they can be called in any component or function with this.$feedbackApiClient.
  inject('feedbackApiClient', feedbackApiClient)
}
