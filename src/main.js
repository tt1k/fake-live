import Vue from 'vue'
import App from './App.vue'

// vuetify
import vuetify from './plugins/vuetify'

// vue-video-player
import VideoPlayer from 'vue-video-player'
import 'vue-video-player/src/custom-theme.css'
import 'video.js/dist/video-js.css'
Vue.use(VideoPlayer)

// vue
Vue.config.productionTip = false
new Vue({
  vuetify,
  VideoPlayer,
  render: h => h(App)
}).$mount('#app')
