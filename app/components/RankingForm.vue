<template>
  <b-container fluid class="h-100">
    <!--     Submit Success -->
    <b-jumbotron
      v-if="submitSuccess && !submitError"
      class="rounded m-0"
      fluid
      bg-variant="success"
      text-variant="dark"
      header="Thanks! Your ranking was submitted successfully"
      lead="Start another ranking?"
    >
      <b-button variant="primary" @click="loadRandomSample">Start!</b-button>
    </b-jumbotron>

    <!--     Submit Error -->
    <b-jumbotron
      v-if="!submitSuccess && submitError"
      class="d-flex justify-content-center h-100 w-100 m-0"
      fluid
      bg-variant="danger"
      text-variant="dark"
      header="Sorry! A problem occurred during your submission..."
      lead="Start another ranking?"
    >
      <b-button variant="primary" @click="loadRandomSample">Start!</b-button>
    </b-jumbotron>

    <!--    Loading Icon -->
    <div
      v-if="loading && !submitSuccess && !submitError"
      class="d-flex justify-content-center h-100 w-100"
    >
      <b-icon
        icon="circle-fill"
        animation="throb"
        variant="dark"
        style="width: 120px; height: 120px"
        class="my-auto"
      />
    </div>
    <!--    Ranking Form -->
    <b-form
      v-else-if="!loading && !submitSuccess && !submitError"
      @submit="onSubmit"
      @reset="onReset"
    >
      <!-- Query -->
      <QueryPanel :query="sample.query" />

      <!-- Image Selection -->
      <b-container>
        <Draggable
          :value="images"
          :group="{ name: 'images', pull: 'clone', put: false, sort: false }"
          class="row text-center no-gutters"
        >
          <b-col
            v-for="imgUrl in images"
            :key="imgUrl"
            v-b-tooltip.hover.bottom="'Click to enlarge'"
            lg="2"
            md="2"
            sm="3"
          >
            <b-link v-b-modal="`modal-${imgUrl}`" href="#">
              <b-img
                :id="`img-${imgUrl}`"
                thumbnail
                fluid
                :src="imgUrl"
                height="130px"
                width="130px"
              />
            </b-link>
            <b-modal
              :id="`modal-${imgUrl}`"
              centered
              :title="sample.query"
              ok-only
              hide-footer
            >
              <b-img
                fluid
                center
                rounded="sm"
                class="border border-dark"
                :src="imgUrl"
              />
            </b-modal>
          </b-col>
        </Draggable>
      </b-container>

      <!-- IMAGE RANKING -->
      <b-container fluid class="p-0 m-0">
        <Draggable
          :list="rankedImages"
          :group="{ name: 'images', put: ranksNotFull }"
          tag="div"
          class="d-flex flex-row justify-content-center mt-1 bg-light ranks h-100 flex-wrap border border-dark rounded"
          @add="addToRankedImages"
        >
          <h1 v-if="showDragabbleHint" class="text-dark my-auto">
            Drag n' Drop Images Here To Rank
          </h1>

          <b-link
            v-for="(imgUrl, idx) in rankedImages"
            v-else
            :key="idx"
            v-b-modal="`modal-${imgUrl}`"
            v-b-tooltip.hover.bottom="'Click to enlarge'"
            href="#"
          >
            <b-avatar
              :id="`ranked-${imgUrl}`"
              :src="imgUrl"
              :badge="`${idx + 1}`"
              rounded="sm"
              size="130px"
              badge-top
              class="ml-1"
            />
          </b-link>
        </Draggable>

        <b-progress
          :max="numRanks"
          show-progress
          variant="success"
          class="mt-1"
        >
          <b-progress-bar :value="rankedImages.length">
            <span>
              Progress:
              <strong>{{ rankedImages.length }} / {{ numRanks }}</strong>
            </span>
          </b-progress-bar>
        </b-progress>
      </b-container>

      <b-form-row class="m-0">
        <b-button-group class="w-100 mt-3">
          <b-button type="submit" variant="primary" :disabled="ranksNotFull">
            <span v-if="ranksNotFull">
              Which images are best described by the following sentence? Please
              rank your Top 10!
            </span>
            <span v-else>Submit Ranking</span>
          </b-button>
          <b-button type="reset" variant="danger">Reset Ranking</b-button>
          <b-button type="button" variant="warning" @click="loadRandomSample">
            Get New Sample
          </b-button>
        </b-button-group>
      </b-form-row>
    </b-form>
  </b-container>
</template>

<script>
// import _ from 'lodash'
import QueryPanel from '~/components/QueryPanel'

export default {
  name: 'RankingForm',
  components: { QueryPanel },
  props: {
    numRanks: {
      type: Number,
      default: 10,
    },
    numImages: {
      type: Number,
      default: 24,
    },
  },
  data() {
    return {
      rankedImages: [],
      images: this.randomImages(this.numImages),
      sample: null,
      loading: true,
      submitSuccess: false,
      submitError: false,
    }
  },
  computed: {
    ranksNotFull() {
      return this.rankedImages.length < this.numRanks
    },
    showDragabbleHint() {
      return this.rankedImages.length === 0
    },
  },
  created() {
    this.loadRandomSample()
  },
  methods: {
    randomImages(n) {
      const res = []
      let i
      for (i = 0; i < n; i++) {
        res.push(`https://picsum.photos/id/${i + 20}/500/500`)
      }
      // return _.shuffle(res)
      return res
    },
    addToRankedImages(evt) {
      // remove duplicates
      // https://stackoverflow.com/questions/9229645/remove-duplicate-values-from-js-array
      this.rankedImages = [...new Set(this.rankedImages)]
    },
    async onSubmit(event) {
      event.preventDefault()
      this.loading = true
      this.submitSuccess = await this.$resultApiClient.store(
        this.sample.id,
        this.rankedImages
      )
      this.submitError = !this.submitSuccess
      this.loading = false
    },
    onReset(event) {
      event.preventDefault()
      this.rankedImages = []
    },
    async loadRandomSample() {
      this.loading = true
      this.submitSuccess = false
      this.submitError = false
      this.rankedImages = []

      this.sample = await this.$sampleApiClient.randomSample()

      this.loading = false
    },
  },
}
</script>

<style scoped>
.ranks {
  min-height: 130px;
}
</style>
