import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  // define the methods
  const resultApiClient = {
    submitResult: async (
      esId,
      rankingData,
      workerId = null,
      assignmentId = null,
      hitId = null
    ) => {
      let mtParams = null
      if (workerId !== null && assignmentId !== null && hitId !== null) {
        mtParams = {
          worker_id: workerId,
          assignment_id: assignmentId,
          hit_id: hitId,
        }
      }
      const result = {
        es_id: esId,
        ranking: rankingData,
        mt_params: mtParams,
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
