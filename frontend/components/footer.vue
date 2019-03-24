<template>
  <v-footer
    dark
    height="auto"
    width="100vw"
    style="margin-bottom: 1vh; poso"
  >
    <v-card
      flat
      tile
      class="black white--text text-xs-center"
      width="100vw"
    >
      <v-card-text>
        <v-btn class="mx-3 white--text button" icon large>
          <img :src="'./../static/Telegram.png'" height="44px" onclick="window.open('https://t.me/politexbot')">
        </v-btn>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-text class="white--text">
        &copy;2019 — <strong>DG team</strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
  export default {
    name: "footer",
    data: () => ({
    }),
    methods: {
      ChangeNet() {
        this.$emit('ChangeNet', this.net);
      }
    }
  }
</script>

<style scoped>
</style>
