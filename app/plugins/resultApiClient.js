import { logger } from './logger'

export default ({ app, axios }, inject) => {
  async function submitResult(type, result, jwt) {
    jwt = JSON.stringify(jwt).replaceAll('"', '')
    const authJsonHeaderConfig = {
      headers: {
        Accept: 'application/json',
        Authorization: 'Bearer ' + jwt,
      },
    }
    return await app.$axios
      .put(
        `${app.$config.ctxPath}api/${type}_result/submit`,
        result,
        authJsonHeaderConfig
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
      hitId = '',
      userId = null,
      jwt = null
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
        sample_id: rsId,
        ranking: rankedImages,
        irrelevant: irrelevantImages,
        mt_params: mtParams,
        user_id: userId,
      }
      return await submitResult('ranking', result, jwt)
    },
    submitLikertResult: async (
      lsId,
      chosenAnswer,
      workerId = '',
      assignmentId = '',
      hitId = '',
      userId = null,
      jwt = null
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
        sample_id: lsId,
        chosen_answer: chosenAnswer,
        mt_params: mtParams,
        user_id: userId,
      }
      return await submitResult('likert', result, jwt)
    },
    submitRatingResult: async (
      rsId,
      imageRatings,
      workerId = '',
      assignmentId = '',
      hitId = '',
      userId = null,
      jwt = null
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
        sample_id: rsId,
        ratings: imageRatings,
        mt_params: mtParams,
        user_id: userId,
      }
      return await submitResult('rating', result, jwt)
    },
    submitRatingWithFocusResult: async (
      rsId,
      contextRatings,
      focusRatings,
      workerId = '',
      assignmentId = '',
      hitId = '',
      userId = null,
      jwt = null
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
        sample_id: rsId,
        context_ratings: contextRatings,
        focus_ratings: focusRatings,
        mt_params: mtParams,
        user_id: userId,
      }
      return await submitResult('rating_with_focus', result, jwt)
    },
  }

  // inject methods so that they can be called in any component or function with this.$resultApiClient.
  inject('resultApiClient', resultApiClient)
}
