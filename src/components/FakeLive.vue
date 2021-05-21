<template>
  <v-container class="pa-0 ma-0 fill-height" fluid>
    <v-row class="ma-0 pa-0">
      <v-col cols="3" class="ma-0 pa-0">
        <v-card color="green light-1">
          <v-treeview
            activatable
            :items="items"
          ></v-treeview>
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
export default {
  name: 'FakeLive',
  data: () => ({
    playerOptions: {
      height: '360',
      autoplay: true,
      muted: true,
      language: 'en',
      playbackRates: [0.7, 1.0, 1.5, 2.0],
      sources: [{
        type: "video/mp4",
        src: "http://vjs.zencdn.net/v/oceans.mp4",
      }],
      poster: "https://surmon-china.github.io/vue-quill-editor/static/images/surmon-1.jpg",
    },
    items: [
      {
        id: 1,
        name: 'Applications :',
        children: [
          { id: 2, name: 'Calendar : app' },
          { id: 3, name: 'Chrome : app' },
          { id: 4, name: 'Webstorm : app' },
        ],
      },
      {
        id: 5,
        name: 'Documents :',
        children: [
          {
            id: 6,
            name: 'vuetify :',
            children: [
              {
                id: 7,
                name: 'src :',
                children: [
                  { id: 8, name: 'index : ts' },
                  { id: 9, name: 'bootstrap : ts' },
                ],
              },
            ],
          },
          {
            id: 10,
            name: 'material2 :',
            children: [
              {
                id: 11,
                name: 'src :',
                children: [
                  { id: 12, name: 'v-btn : ts' },
                  { id: 13, name: 'v-card : ts' },
                  { id: 14, name: 'v-window : ts' },
                ],
              },
            ],
          },
        ],
      },
      {
        id: 15,
        name: 'Downloads :',
        children: [
          { id: 16, name: 'October : pdf' },
          { id: 17, name: 'November : pdf' },
          { id: 18, name: 'Tutorial : html' },
        ],
      },
      {
        id: 19,
        name: 'Videos :',
        children: [
          {
            id: 20,
            name: 'Tutorials :',
            children: [
              { id: 21, name: 'Basic layouts : mp4' },
              { id: 22, name: 'Advanced techniques : mp4' },
              { id: 23, name: 'All about app : dir' },
            ],
          },
          { id: 24, name: 'Intro : mov' },
          { id: 25, name: 'Conference introduction : avi' },
        ],
      },
    ],
  }),
}
</script>
