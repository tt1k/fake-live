<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          :src="require('./assets/logo.png')"
          transition="scale-transition"
          width="50"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="180"
          :src="require('./assets/fakelive.png')"
          width="180"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn-toggle mandatory background-color="primary">
        <v-col v-for="(continent, index) in continent_list" :key="index">
          <v-btn class="white--text rounded-lg font-weight-black" btn-toggle-btn-padding="0 0px" :value="index" color="blue lighten-1">{{continent}}</v-btn>
        </v-col>
      </v-btn-toggle>

      <v-spacer></v-spacer>

      <v-btn href="https://github.com/IcedOtaku/fake-live" target="_blank" text>
        <span class="mr-2">Github</span>
        <v-icon>mdi-github</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <FakeLive/>
    </v-main>
  </v-app>
</template>

<script>
import FakeLive from "./components/FakeLive";

export default {
  name: 'App',
  components: {
    FakeLive,
  },
  data: () => ({
    continent_list: [
      "Asia",
      "Europe",
      "North America",
      "South America",
      "Africa",
      "Oceania",
      "Antarctica"
    ]
  }),
};
</script>
