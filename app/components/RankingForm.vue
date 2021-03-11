<template>
  <b-container fluid class="h-100">
    <!--     Submit Success Jumbotron -->
    <b-jumbotron
      v-if="submitSuccess && !submitError"
      class="rounded m-0"
      fluid
      bg-variant="success"
      text-variant="dark"
      header="Thanks! Your ranking was submitted successfully"
      lead="Start another ranking?"
    >
      <b-button v-if="esId === null" variant="primary" @click="loadNextSample"
        >Start!</b-button
      >
    </b-jumbotron>

    <!--     Submit Error Jumbotron -->
    <b-jumbotron
      v-if="!submitSuccess && submitError"
      class="rounded m-0"
      fluid
      bg-variant="danger"
      text-variant="dark"
      header="Sorry! A problem occurred during your submission..."
      lead="Start another ranking?"
    >
      <b-button v-if="esId === null" variant="primary" @click="loadNextSample"
        >Start!</b-button
      >
    </b-jumbotron>

    <!--     Load Error Jumbotron -->
    <b-jumbotron
      v-if="!loadSuccess && loadError"
      class="rounded m-0"
      fluid
      bg-variant="danger"
      text-variant="dark"
      header="Sorry! A problem occurred while loading your evaluation sample..."
      lead="Please start another ranking!"
    >
      <b-button v-if="esId === null" variant="primary" @click="loadNextSample"
        >Start!</b-button
      >
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
        class="my-auto ranks"
      />
    </div>

    <!--    Ranking Form -->
    <b-form
      v-else-if="!loading && loadSuccess && !loadError"
      @submit="onSubmit"
      @reset="onReset"
    >
      <!-- Image Selection -->
      <b-container
        fluid
        style="max-height: 550px"
        class="overflow-auto border border-dark rounded-top bg-secondary p-3"
      >
        <Draggable
          :value="imageUrls"
          :group="{ name: 'images', pull: 'clone', put: false, sort: false }"
          class="row text-center no-gutters"
        >
          <b-col
            v-for="imgUrl in imageUrls"
            :key="imgUrl"
            class="mt-1"
            lg="2"
            md="3"
            sm="4"
            :style="`min-width: ${img_size}px; min-height: ${img_size}px`"
          >
            <b-link v-b-modal="`modal-${imgUrl}`" href="#">
              <b-img
                :id="`img-${imgUrl}`"
                v-b-tooltip.hover.bottom="'Click to enlarge'"
                thumbnail
                rounded
                :src="imgUrl"
                :style="`
                  max-width: ${img_size}px;
                  max-height: ${img_size}px;
                  min-width: ${img_size}px;
                  min-height: ${img_size}px;
                  `"
              />
            </b-link>
            <b-modal
              :id="`modal-${imgUrl}`"
              centered
              ok-only
              hide-header
              size="lg"
              footer-bg-variant="dark"
              footer-text-variant="light"
            >
              <b-img
                fluid
                center
                rounded="sm"
                class="border border-dark"
                :src="imgUrl"
              />
              <template #modal-footer>
                <p>{{ sample.query }}</p>
              </template>
            </b-modal>
          </b-col>
        </Draggable>
      </b-container>

      <!-- Query -->
      <h4
        class="p-2 border border-dark rounded-bottom bg-info font-italic"
        :style="`height: ${img_size + 10}px;`"
      >
        {{ sample.query }}
      </h4>

      <!-- IMAGE RANKING -->
      <b-container fluid class="p-1 fixed-bottom">
        <Draggable
          :list="rankedImages"
          :group="{ name: 'images', put: ranksNotFull }"
          tag="div"
          class="d-flex flex-row flex-nowrap justify-content-center mt-1 bg-light border border-dark h-100 rounded overflow-auto"
          :style="`min-height: ${img_size}px;
           max-height: ${img_size + 15}px; max-width: 100vw`"
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
            v-b-tooltip.hover.bottom.html="
              'Click to enlarge </br> Right-click to remove'
            "
            href="#"
            size="lg"
            @contextmenu="removeRankedImage($event, imgUrl)"
          >
            <b-avatar
              :id="`ranked-${imgUrl}`"
              :src="imgUrl"
              :badge="`${idx + 1}`"
              rounded="sm"
              :size="`${img_size}px`"
              badge-top
              class="ml-1 border border-dark border"
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

        <!-- FORM BUTTONS -->
        <b-form-row class="m-0">
          <b-button-group class="w-100 mt-1 mb-1">
            <b-button type="submit" variant="primary" :disabled="ranksNotFull">
              <span v-if="ranksNotFull">
                Which images are best described by the caption? Please rank your
                Top {{ numRanks }}!
              </span>
              <span v-else>Submit Ranking</span>
            </b-button>
            <b-button type="reset" variant="danger">Reset Ranking</b-button>
            <b-button
              v-if="esId === null"
              type="button"
              variant="warning"
              @click="loadNextSample"
            >
              Get New Sample
            </b-button>
          </b-button-group>
        </b-form-row>
      </b-container>
    </b-form>
  </b-container>
</template>

<script>
export default {
  name: 'RankingForm',
  props: {
    numRanks: {
      type: Number,
      default: 10,
    },
    numImages: {
      type: Number,
      default: 24,
    },
    esId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      rankedImages: [],
      imageUrls: [],
      sample: null,
      loading: true,
      submitSuccess: false,
      submitError: false,
      loadSuccess: false,
      loadError: false,
      img_size: 120,
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
    if (this.esId === null) this.loadNextSample()
    else this.loadSample()
  },
  methods: {
    removeRankedImage(evt, imgUrl) {
      evt.preventDefault()
      const pos = this.rankedImages.indexOf(imgUrl)
      this.rankedImages.splice(pos, 1)
    },
    addToRankedImages(evt) {
      // remove duplicates
      // https://stackoverflow.com/questions/9229645/remove-duplicate-values-from-js-array
      this.rankedImages = [...new Set(this.rankedImages)]
    },
    getImageIds(urls) {
      return this.$imageApiClient.getIds(urls)
    },
    onReset(event) {
      event.preventDefault()
      this.rankedImages = []
    },
    async onSubmit(event) {
      event.preventDefault()
      this.loading = true
      this.submitError = false
      this.submitSuccess = false

      const ids = await this.getImageIds(this.rankedImages)
      this.submitSuccess = await this.$resultApiClient.submitResult(
        this.sample.id,
        ids
      )
      this.submitError = !this.submitSuccess
      this.loadError = false
      this.loadSuccess = false
      this.loading = false

      this.$nuxt.$emit('study-progress-changed')
    },
    async loadNextSample() {
      this.loading = true
      this.loadSuccess = false
      this.loadError = false
      this.submitError = false
      this.submitSuccess = false

      this.rankedImages = []

      this.sample = await this.$sampleApiClient.nextSample()
      this.loadSuccess = this.sample !== null
      this.loadError = !this.loadSuccess

      if (this.loadSuccess)
        this.imageUrls = await this.$imageApiClient.getUrls(
          this.sample.image_ids
        )

      this.loading = false

      this.$nuxt.$emit('study-progress-changed')
    },
    async loadSample() {
      this.loading = true
      this.loadSuccess = false
      this.loadError = false
      this.submitError = false
      this.submitSuccess = false

      this.rankedImages = []

      this.sample = await this.$sampleApiClient.load(this.esId)
      this.loadSuccess = this.sample !== null
      this.loadError = !this.loadSuccess

      if (this.loadSuccess)
        this.imageUrls = await this.$imageApiClient.getUrls(
          this.sample.image_ids
        )

      this.loading = false

      this.$nuxt.$emit('study-progress-changed')
    },
  },
}
</script>

<style scoped>
.ranks {
  min-height: 7.5em !important;
  max-height: 7.5em !important;
  min-width: 7.5em !important;
  max-width: 7.5em !important;
}
</style>
