// define the methods
export const logger = (lvl, msg) => {
  const m = JSON.stringify(msg)
  if (lvl === 'error' || lvl === 'err' || lvl === 'e')
    try {
      window.console.error(m)
    } catch (e) {
      // window not defined
      // eslint-disable-next-line no-console
      console.error(m)
    }
  else if (lvl === 'warning' || lvl === 'warn' || lvl === 'w')
    try {
      window.console.warn(m)
    } catch (e) {
      // window not defined
      // eslint-disable-next-line no-console
      console.warn(m)
    }
  else if (lvl === 'info' || lvl === 'i')
    try {
      window.console.info(m)
    } catch (e) {
      // window not defined
      // eslint-disable-next-line no-console
      console.info(m)
    }
}

export default ({ app }, inject) => {
  // inject methods so that they can be called in any component or function with this.$logger.
  inject('logger', logger)
}
