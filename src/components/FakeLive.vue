<template>
  <v-container class="ma-0 pa-0" fluid fill-height>
    <v-row class="ma-0 pa-0">
      <v-col cols="2" class="ma-0 pa-0 pr-4">
        <v-card class="font-weight-black">
          <v-treeview
            activatable
            :items="channelItemLists">
            <template slot="label" slot-scope="{ item }">
              <a @click="clickChannel(item)">{{ item.name }}</a>
            </template>
          </v-treeview>
        </v-card>
      </v-col>

      <v-col cols="10" class="ma-0 pa-0">
        <v-card color="green light-1">
          <video-player
            ref="videoPlayer"
            class="vjs-custom-skin"
            crossOrigin="Anonymous"
            :options="playerOptions"
            @play="onPlayerPlay($event)"
            @pause="onPlayerPause($event)"
            @waiting="onPlayerWaiting($event)"
            @loadeddata="onPlayerLoadeddata($event)"
            @playing="onPlayerPlaying($event)"
            @canplay="onPlayerCanplay($event)"
            @ready="onPlayerReadied">
          </video-player>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="ma-0 pa-0" align="center" justify="center">
      <v-col class="ma-0 pa-0">
        <p class="ma-0 pa-0 font-weight-black" align="center">
          Channel: {{playerSourceName}}
        </p>
        <p class="ma-0 pa-0 font-weight-black subtitle-2" align="center">
          URL: {{playerSourceURL}}
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  // videojs
  import videojs from 'video.js'
  window.videojs = videojs
  // hls plugin for videojs6
  require('videojs-contrib-hls/dist/videojs-contrib-hls.js')
  // json data
  import channel_source_json from '../../shell/build/fake_live_success.json'

  export default {
    name: 'FakeLive',
    data: () => ({
      playerSourceURL: "Please select video source",
      playerSourceName: "Please select video source",
      playerOptions: {
        height: 800,
        sources: [{
          withCredentials: false,
          type: "application/x-mpegURL",
          src: "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8"
        }],
        controlBar: {
          timeDivider: false,
          durationDisplay: false
        },
        flash: { hls: { withCredentials: false }},
        html5: { hls: { withCredentials: false }},
        poster: require('../assets/fakelive-bg.png')
      },
      channelItemLists: channel_source_json
    }),
    computed: {
      player() {
        return this.$refs.videoPlayer.player
      }
    },
    methods: {
      clickChannel(channelItem) {
        console.log(channelItem.name, channelItem.url)
        let player = this.$refs.videoPlayer.player
        player.src(channelItem.url)
        this.playerSourceURL = channelItem.url
        this.playerSourceName = channelItem.name
        console.log("[vue-video-player]: the player source has been changed to", channelItem.url)
      },
      onPlayerPlay(player) {
        console.log("[vue-video-player]: the player is started", player)
      },
      onPlayerPause(player) {
        console.log("[vue-video-player]: the player is stopped", player)
      },
      onPlayerReadied(player) {
        console.log("[vue-video-player]: the player is readied", player)
      },
      onPlayerWaiting(player) {
        console.log("[vue-video-player]: the player is loading", player)
      },
      onPlayerLoadeddata(player) {
        console.log("[vue-video-player]: the player has loaded all data", player)
      },
      onPlayerCanplay(player) {
        console.log("[vue-video-player]: the player is able to play", player)
      },
      onPlayerPlaying(player) {
        console.log("[vue-video-player]: the player is now playing", player)
      },
    }
  }
</script>