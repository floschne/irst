<template>
  <b-container fluid>
    <b-row class="text-center" no-gutters>
      <b-col v-for="rank in num_ranks" :key="rank">
        <div class="rank bg-light align-middle">
          <b-badge pill variant="primary">
            {{ rank }}
          </b-badge>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'RankingPanel',
  props: {
    num_ranks: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      ranking: [],
    }
  },
}
</script>

<style scoped>
.rank {
  width: 130px;
  height: 130px;
}
</style>
