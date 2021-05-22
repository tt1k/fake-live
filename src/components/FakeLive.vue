<template>
  <v-container>
    <v-row class="ma-0 pa-0">
      <v-col cols="3" class="ma-0 pa-0">
        <v-card color="green light-1">
          <v-treeview
            activatable
            :items="channelItemLists">
            <template slot="label" slot-scope="{ item }">
              <a @click="clickChannel(item)">{{ item.name }}</a>
            </template>
          </v-treeview>
        </v-card>
      </v-col>

      <v-col cols="9" class="ma-0 pa-0">
        <v-card color="green light-1">
          <video-player class="vjs-custom-skin" :options="playerOptions">
          </video-player>
        </v-card>
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

  export default {
    name: 'FakeLive',
    data: () => ({
      playerOptions: {
        height: '720',
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
      channelItemLists: [
        {
          id: 1,
          name: "North America",
          children: [
            {
              name: "United States (US)",
              children: [
                {
                  name: "AMC | IFC Film Picks",
                  url: "https://amc-ifc-films-picks-1.imdbtv.wurl.com/manifest/playlist.m3u8"
                },
                {
                  name: "AMC IFC Film Picks",
                  url: "https://amc-ifc-films-picks-1.vizio.wurl.com/manifest/playlist.m3u8"
                },
              ]
            },
          ],
        },
        {
          id: 2,
          name: "Asia",
          children: [
            {
              name: "Kazakhstan (KZ)",
              children: [
                {
                  name: "Amedia Hit",
                  url: "http://sc.id-tv.kz:80/amedia_hit_hd_38_39.m3u8"
                },
              ]
            },
            {
              name: "China (CN)",
              children: [
                {
                  name: "CCTV-1\u7efc\u5408",
                  url: "http://183.207.248.71:80/cntv/live1/CCTV-1/cctv-1"
                },
                {
                  name: "CCTV\u4e2d\u56fd\u4e2d\u592e\u7535\u89c6\u53f0-1 \u7efc\u5408",
                  url: "http://125.210.152.10:8060/live/CCTV1HD_H265.m3u8"
                }
              ]
            }
          ],
        },
      ],
    }),
    methods: {
      clickChannel(channelItem) {
        console.log(channelItem.name, channelItem.url)
        this.playerOptions.sources.url = channelItem.url
      }
    }
  }
</script>