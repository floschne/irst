<template>
  <b-container class="text-center">
    <LoginForm v-if="jwt === null" class="mt-5" @auth-success="loadProgress" />
    <div v-if="success">
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
    <!-- Error Jumbotron -->
    <b-jumbotron
      v-if="!success && jwt !== null"
      class="rounded m-0"
      fluid
      bg-variant="danger"
      text-variant="dark"
      header="Could not authenticate!"
      :lead="errorMessage"
    ></b-jumbotron>
  </b-container>
</template>

<script>
import LoginForm from '~/components/LoginForm'
export default {
  name: 'Status',
  components: { LoginForm },
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
      success: false,
      jwt: null,
      errorMessage: null,
    }
  },
  methods: {
    async loadProgress(jwt) {
      this.success = false
      if (this.jwt === null) this.jwt = jwt
      const resp = await this.$studyApiClient.getProgress(this.jwt)
      if ('num_todo' in resp) {
        this.success = true
        this.progress = resp
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
      } else if ('detail' in resp) {
        this.errorMessage = resp.detail
        this.jwt = null
        this.success = false
        this.progress = null
      }
    },
  },
}
</script>

<style scoped></style>
