import { logger } from './logger'

export default ({ $axios }) => {
  $axios.onResponse((response) => {
    logger('i', `[${response.status}] ${response.request.path}`)
  })

  $axios.onError((err) => {
    logger(
      'e',
      `[${err.response && err.response.status}] ${
        err.response && err.response.request.path
      }`
    )
    logger('e', err.response && err.response.data)
  })
}
