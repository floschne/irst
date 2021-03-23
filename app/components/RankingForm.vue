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
        class="overflow-auto border border-dark rounded-top bg-secondary p-1"
      >
        <Draggable
          :value="thumbnailUrls"
          :group="{ name: 'images', pull: 'clone', put: false, sort: false }"
          class="row text-center no-gutters"
        >
          <b-col
            v-for="(tnUrl, idx) in thumbnailUrls"
            :key="`tn-col-${idx}`"
            class="mt-1 d-flex justify-content-center"
            lg="1"
            md="2"
            sm="3"
            :style="`min-width: ${img_size}rem; min-height: ${img_size}rem`"
          >
            <b-link href="#" class="image-container ranks">
              <b-img
                :id="`tn-img-${idx}`"
                v-b-modal="`modal-${tnUrl}`"
                thumbnail
                rounded
                :src="tnUrl"
                class="ranks"
                @contextmenu="tagAsIrrelevant($event, tnUrl)"
              />
              <div
                v-b-tooltip.hover.top="'Click to untag'"
                :class="`image-overlay ranks ranks
                ${imageOverlayBgVariant(tnUrl)}
                ${imageOverlayDisplay(tnUrl)}`"
                @click="removeOrUntagImage($event, tnUrl)"
                @contextmenu="removeOrUntagImage($event, tnUrl)"
              >
                <b-icon
                  :icon="`${imageOverlayIcon(tnUrl)}-circle`"
                  variant="dark"
                  font-scale="6.5"
                  class="image-overlay-icon"
                />
              </div>

              <b-tooltip
                :target="`tn-img-${idx}`"
                :show.sync="tooltipStates[`tn-img-${idx}`]"
                placement="top"
                triggers="hover"
                noninteractive
              >
                Click to enlarge <br />
                Right-click to tag as irrelevant
              </b-tooltip>
            </b-link>
            <b-modal
              :id="`modal-${tnUrl}`"
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
                :src="imageUrls[idx]"
                style="max-height: 60vh"
              />
              <template #modal-footer>
                <p>{{ sample.query }}</p>
              </template>
            </b-modal>
          </b-col>
        </Draggable>
      </b-container>

      <!-- Query -->
      <h5
        class="p-1 border border-dark rounded-bottom bg-info font-italic text-center"
        style="max-height: 100px; overflow-y: scroll"
      >
        {{ sample.query }}
      </h5>

      <!-- IMAGE RANKING -->
      <b-container id="imageRankingFooter" fluid class="p-1 fixed-bottom">
        <Draggable
          :list="rankedImages"
          :group="{ name: 'images' }"
          tag="div"
          class="d-flex flex-row flex-nowrap justify-content-center align-items-center mt-1 bg-light border border-dark h-100 rounded overflow-auto"
          :style="`min-height: ${img_size}rem;
           max-height: ${img_size + 1}rem; max-width: 100vw`"
          @add="addToRankedImages"
        >
          <div
            v-if="showDragabbleHint"
            class="text-dark"
            style="font-size: 2.75vw"
          >
            Drag n' Drop Images Here To Rank From Highest To Lowest
          </div>

          <b-link
            v-for="(tnUrl, idx) in rankedImages"
            v-else
            :key="idx"
            v-b-modal="`modal-${tnUrl}`"
            v-b-tooltip.hover.topright.html="
              'Click to enlarge </br> Right-click to remove'
            "
            href="#"
            :size="`${img_size}rem`"
            @contextmenu="removeOrUntagImage($event, tnUrl)"
          >
            <b-avatar
              :id="`ranked-${tnUrl}`"
              :src="tnUrl"
              :badge="`${idx + 1}`"
              rounded="sm"
              :size="`${img_size}rem`"
              badge-top
              class="ml-1 border border-dark border"
            />
          </b-link>
        </Draggable>

        <b-progress
          :max="imageUrls.length"
          show-progress
          variant="success"
          class="mt-1"
        >
          <b-progress-bar
            :value="rankedImages.length + irrelevantImages.length"
          >
            <span>
              Progress:
              <strong>
                {{ rankedImages.length + irrelevantImages.length }} /
                {{ imageUrls.length }}
              </strong>
            </span>
          </b-progress-bar>
        </b-progress>

        <!-- FORM BUTTONS -->
        <b-form-row class="m-0 text-center">
          <h3 v-if="hitPreview" class="text-warning bg-dark w-100">
            You must accept this HIT before working on it!
          </h3>
          <b-button-group v-else class="w-100 mt-1 mb-1">
            <b-button
              type="submit"
              variant="primary"
              :disabled="submitDisabled"
            >
              <div
                v-if="submitDisabled"
                class="w-100"
                @click="showMinNumRanksNotPossibleToast"
              >
                Which images are best described by the caption? Please rank your
                top images and tag irrelevant images!
              </div>
              <span v-else>Submit Ranking</span>
            </b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
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
    <form id="hiddenMTurkForm" method="post" :action="mturkExternalSubmitUrl">
      <input
        id="assignmentId"
        type="hidden"
        name="assignmentId"
        :value="assignmentId"
      />
      <input id="erId" type="hidden" name="erId" :value="erId" />
    </form>
  </b-container>
</template>

<script>
export default {
  name: 'RankingForm',
  props: {
    minNumRanks: {
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
    assignmentId: {
      type: String,
      default: null,
    },
    workerId: {
      type: String,
      default: null,
    },
    hitId: {
      type: String,
      default: null,
    },
  },
  emits: ['study-progress-changed'],
  data() {
    return {
      rankedImages: [],
      irrelevantImages: [],
      imageUrls: [],
      thumbnailUrls: [],
      sample: null,
      loading: true,
      submitSuccess: false,
      submitError: false,
      loadSuccess: false,
      loadError: false,
      img_size: 7.5,
      erId: '',
      tooltipStates: {},
    }
  },
  computed: {
    submitDisabled() {
      const allProcessed =
        this.irrelevantImages.length + this.rankedImages.length ===
        this.imageUrls.length
      return !allProcessed || this.rankedImages.length < this.minNumRanks
    },
    showDragabbleHint() {
      return this.rankedImages.length === 0
    },
    hitPreview() {
      return this.assignmentId === 'ASSIGNMENT_ID_NOT_AVAILABLE'
    },
    mturkExternalSubmitUrl() {
      const sub = this.$config.mturkSandbox ? 'workersandbox' : 'www'
      return `https://${sub}.mturk.com/mturk/externalSubmit`
    },
  },
  created() {
    if (this.esId === null) this.loadNextSample()
    else this.loadSample()
  },
  methods: {
    addToRankedImages(evt) {
      evt.preventDefault()
      this.hideTooltip(evt.oldIndex)
      // remove duplicates
      // https://stackoverflow.com/questions/9229645/remove-duplicate-values-from-js-array
      this.rankedImages = [...new Set(this.rankedImages)]
      // if one of ranked is in irrelevant, remove from irrelevant
      // https://stackoverflow.com/questions/1885557/simplest-code-for-array-intersection-in-javascript
      const intersection = this.irrelevantImages.filter((value) =>
        this.rankedImages.includes(value)
      )
      // there should always only be exactly one element
      if (intersection.length === 1) this.untagAsIrrelevant(intersection[0])
    },
    hideTooltip(idx) {
      // this.$nuxt.$emit('bv::tooltip::hide', `tn-img-${idx}`)  FIXME event gets emitted but without any effect
      this.tooltipStates[`tn-img-${idx}`] = false
    },
    removeRankedImage(tnUrl) {
      const pos = this.rankedImages.indexOf(tnUrl)
      this.rankedImages.splice(pos, 1)
    },
    tagAsIrrelevant(evt, tnUrl) {
      evt.preventDefault()
      this.irrelevantImages.push(tnUrl)
      // remove duplicates
      // https://stackoverflow.com/questions/9229645/remove-duplicate-values-from-js-array
      this.irrelevantImages = [...new Set(this.irrelevantImages)]
      // if the number of irrelevant images wouldn't allow the minimum number of ranked images, reject and show toast
      if (
        this.irrelevantImages.length >
        this.imageUrls.length - this.minNumRanks
      ) {
        this.untagAsIrrelevant(tnUrl)
        this.showMinNumRanksNotPossibleToast()
      }
    },
    untagAsIrrelevant(tnUrl) {
      const pos = this.irrelevantImages.indexOf(tnUrl)
      this.irrelevantImages.splice(pos, 1)
    },
    removeOrUntagImage(evt, tnUrl) {
      evt.preventDefault()
      if (this.irrelevantImages.includes(tnUrl)) this.untagAsIrrelevant(tnUrl)
      else if (this.rankedImages.includes(tnUrl)) this.removeRankedImage(tnUrl)
    },
    getImageIds(urls) {
      return this.$imageApiClient.getIds(urls)
    },
    onReset(event) {
      event.preventDefault()
      this.rankedImages = []
      this.irrelevantImages = []
    },
    async onSubmit(event) {
      event.preventDefault()
      this.loading = true
      this.submitError = false
      this.submitSuccess = false

      // get the ids from URLs
      const rankedIds = await this.getImageIds(this.rankedImages)
      const irrelevantIds = await this.getImageIds(this.irrelevantImages)
      // submit to own API
      this.erId = await this.$resultApiClient.submitResult(
        this.sample.id,
        rankedIds,
        irrelevantIds,
        this.workerId,
        this.assignmentId,
        this.hitId
      )
      this.submitSuccess =
        this.erId !== null && this.erId !== undefined && this.erId !== ''
      this.submitError = !this.submitSuccess

      // submit to MTurk if in MTurk mode
      if (this.submitSuccess && this.assignmentId !== null) {
        // via axios
        // fixme currently not working because we would have to follow the redirect and set the cookie correctly
        // fixme see the last comment (from AWS staff) https://forums.aws.amazon.com/thread.jspa?messageID=553442
        // fixme we COULD get this working but it would be PITA
        //   this.submitSuccess = await this.$mturkSubmitService.submitAssignment(
        //     ids,
        //     this.assignmentId,
        //     this.erId
        //   )
        //   this.submitError = !this.submitSuccess
        // via cgi html form
        document.getElementById('hiddenMTurkForm').submit()
      }

      // reset flags
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
      this.irrelevantImages = []

      this.sample = await this.$sampleApiClient.nextSample()
      this.loadSuccess = this.sample !== null
      this.loadError = !this.loadSuccess

      if (this.loadSuccess) {
        // load image urls
        this.imageUrls = await this.$imageApiClient.getUrls(
          this.sample.image_ids,
          false
        )
        // load thumbnail urls
        this.thumbnailUrls = await this.$imageApiClient.getUrls(
          this.sample.image_ids,
          true
        )
        // init tooltip states
        this.thumbnailUrls.forEach((tnUrl, idx) => {
          this.tooltipStates[`tn-img-${idx}`] = false
        })
      }

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
      this.irrelevantImages = []

      this.sample = await this.$sampleApiClient.load(this.esId)
      this.loadSuccess = this.sample !== null
      this.loadError = !this.loadSuccess

      if (this.loadSuccess) {
        // load image urls
        this.imageUrls = await this.$imageApiClient.getUrls(
          this.sample.image_ids,
          false
        )
        // load thumbnail urls
        this.thumbnailUrls = await this.$imageApiClient.getUrls(
          this.sample.image_ids,
          true
        )
      }

      this.loading = false

      this.$nuxt.$emit('study-progress-changed')
    },
    imageOverlayDisplay(tnUrl) {
      return this.rankedImages.includes(tnUrl) ||
        this.irrelevantImages.includes(tnUrl)
        ? 'd-flex'
        : 'd-none'
    },
    imageOverlayIcon(tnUrl) {
      if (this.rankedImages.includes(tnUrl)) return 'check'
      else if (this.irrelevantImages.includes(tnUrl)) return 'x'
    },
    imageOverlayBgVariant(tnUrl) {
      if (this.rankedImages.includes(tnUrl)) return 'bg-success'
      else if (this.irrelevantImages.includes(tnUrl)) return 'bg-danger'
    },
    showMinNumRanksNotPossibleToast() {
      this.$nuxt.$bvToast.toast(
        `Please RANK AT LEAST YOUR TOP ${this.minNumRanks} images AND TAG ALL THE REMAINING images as irrelevant! For instructions, please click the (?) on the top-left`,
        {
          title: 'Invalid Data!',
          autoHideDelay: 5000,
          appendToast: true,
          variant: 'danger',
          solid: true,
          toaster: 'b-toaster-top-full',
        }
      )
    },
  },
}
</script>

<style scoped>
.ranks {
  min-height: 7.5rem !important;
  max-height: 7.5rem !important;
  min-width: 7.5rem !important;
  max-width: 7.5rem !important;
}

.image-container {
  position: relative;
  text-align: center;
  width: 100%;
}

.image-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  width: 100%;
  text-align: center;
  opacity: 0.75;
  transition: 0.3s ease;
  z-index: 999;
}

.image-overlay-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
}
</style>
