import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const formDataHeaderConfig = {
    headers: { 'Content-Type': 'multipart/form-data' },
  }
  // define the methods
  const mturkSubmitService = {
    submitAssignment: async (submitUrl, ranking, assignmentId, erId) => {
      // https://stackoverflow.com/questions/47630163/axios-post-request-to-send-form-data
      const bodyFormData = new FormData()
      bodyFormData.append('assignmentId', assignmentId)
      bodyFormData.append('erId', erId)
      bodyFormData.append('ranking', ranking)
      try {
        const resp = await app.$axios.post(
          submitUrl,
          bodyFormData,
          formDataHeaderConfig
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

  // inject methods so that they can be called in any component or function with this.$mturkSubmitService.
  inject('mturkSubmitService', mturkSubmitService)
}
