const proxyConfig = () => {
  let proxyTarget = ''

  if (process.env.APP_DEPLOY === 'docker') {
    const dockerApiHost = process.env.API_HOST
    const dockerApiPort = process.env.API_PORT

    proxyTarget = 'http://' + dockerApiHost + ':' + dockerApiPort + '/'
  } else {
    proxyTarget = 'http://localhost:8081/'
  }

  return {
    '/api/': {
      target: proxyTarget,
      pathRewrite: { '^/api/': '' },
    },
  }
}

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Image Ranking User Study',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'Image Ranking User Study WebApp',
      },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '@/plugins/generalApiClient.js' },
    { src: '@/plugins/resultApiClient.js' },
    { src: '@/plugins/sampleApiClient.js' },
    { src: '@/plugins/imageApiClient.js' },
    { src: '@/plugins/studyApiClient.js' },
    { src: '@/plugins/vuedraggable.js' },
    { src: '@/plugins/vuechart.js' },
    { src: '@/plugins/logger.js' },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
  ],

  // https://github.com/nuxt-community/proxy-module#readme
  // necessary for CORS
  proxy: proxyConfig(),

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    proxy: true,
  },

  // https://bootstrap-vue.org/docs#icons
  bootstrapVue: {
    icons: true, // Install the IconsPlugin (in addition to BootStrapVue plugin
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  router: {
    base: process.env.APP_CTX_PTH,
  },

  server: {
    port: 3000, // default: 3000
    host: '0.0.0.0', // default: localhost,
    timing: false,
  },
}
