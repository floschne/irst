import { logger } from './logger'

export default ({ app, axios }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
    },
  }

  async function submitResult(type, result) {
    return await app.$axios
      .put(
        `${app.$config.ctxPath}api/${type}_result/submit`,
        result,
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
  }

  // define the methods
  const resultApiClient = {
    submitRankingResult: async (
      rsId,
      rankedImages,
      irrelevantImages,
      workerId = '',
      assignmentId = '',
      hitId = ''
    ) => {
      let mtParams = null
      if (workerId !== '' && assignmentId !== '' && hitId !== '') {
        mtParams = {
          worker_id: workerId,
          assignment_id: assignmentId,
          hit_id: hitId,
        }
      }
      const result = {
        rs_id: rsId,
        ranking: rankedImages,
        irrelevant: irrelevantImages,
        mt_params: mtParams,
      }
      return await submitResult('ranking', result)
    },
    submitLikertResult: async (
      lsId,
      chosenAnswer,
      workerId = '',
      assignmentId = '',
      hitId = ''
    ) => {
      let mtParams = null
      if (workerId !== '' && assignmentId !== '' && hitId !== '') {
        mtParams = {
          worker_id: workerId,
          assignment_id: assignmentId,
          hit_id: hitId,
        }
      }
      const result = {
        ls_id: lsId,
        chosen_answer: chosenAnswer,
        mt_params: mtParams,
      }
      return await submitResult('ranking', result)
    },
    submitRatingResult: async (
      rsId,
      imageRatings,
      workerId = '',
      assignmentId = '',
      hitId = ''
    ) => {
      let mtParams = null
      if (workerId !== '' && assignmentId !== '' && hitId !== '') {
        mtParams = {
          worker_id: workerId,
          assignment_id: assignmentId,
          hit_id: hitId,
        }
      }
      const result = {
        rs_id: rsId,
        ratings: imageRatings,
        mt_params: mtParams,
      }
      return await submitResult('ranking', result)
    },
  }

  // inject methods so that they can be called in any component or function with this.$resultApiClient.
  inject('resultApiClient', resultApiClient)
}
