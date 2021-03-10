<template>
  <b-container class="text-center">
    <div v-if="!loading && success">
      <DoughnutChart
        :data="chartData"
        :options="chartOptions"
        :styles="chartStyles"
      />
      <div class="w-100 fixed-bottom mt-3 mb-1">
        <h1 class="">Current Study Run: {{ progress.run }}</h1>
        <b-button variant="info" @click="loadProgress">Refresh</b-button>
      </div>
    </div>

    <h1 v-else>Loading...</h1>
  </b-container>
</template>

<script>
export default {
  name: 'Status',
  data() {
    return {
      chartData: {},
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      },
      chartStyles: {
        height: '800px',
      },
      progress: {},
      loading: false,
      success: false,
    }
  },
  created() {
    this.loadProgress()
    this.$nuxt.$on('study-progress-changed', this.loadProgress)
  },
  beforeDestroy() {
    this.$nuxt.$off('study-progress-changed')
  },
  methods: {
    asd() {},
    async loadProgress() {
      this.loading = true
      this.success = false

      this.progress = await this.$studyApiClient.getProgress()

      // see https://www.chartjs.org/docs/latest/charts/doughnut.html#data-structure
      this.chartData = {
        datasets: [
          {
            data: [
              this.progress.num_todo,
              this.progress.num_in_progress,
              this.progress.num_done,
            ],
            backgroundColor: [
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(255, 99, 132)',
            ],
          },
        ],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: ['ToDo', 'In Progress', 'Done'],
      }

      this.success = true
      this.loading = false
    },
  },
}
</script>

<style scoped></style>
