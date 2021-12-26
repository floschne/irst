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
      <b-button v-if="rsId === ''" variant="primary" @click="loadNextSample">
        Start!
      </b-button>
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
      <b-button v-if="rsId === ''" variant="primary" @click="loadNextSample"
        >Start!
      </b-button>
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
      <b-button v-if="rsId === ''" variant="primary" @click="loadNextSample">
        Start!
      </b-button>
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
        class="my-auto image-size"
      />
    </div>

    <!-- Next Sample Waiting Time -->
    <div
      v-if="sample_cooldown > 0"
      class="d-flex justify-content-center h-100 w-100"
    >
      Next Sample is available in
      <span class="badge badge-info p-1 mr-2 ml-2">
        {{ sample_cooldown }}
      </span>
      seconds...
    </div>

    <!--  RATING WITH FOCUS FORM   -->
    <b-form
      v-else-if="!loading && loadSuccess && !loadError"
      @submit="onSubmit"
    >
      <!-- Main Container -->
      <b-container
        fluid
        style="max-height: 800px"
        class="overflow-auto border border-dark rounded-top bg-secondary pt-0"
      >
        <!--  PROGRESS BAR  -->
        <b-row class="mb-1">
          <b-col class="ml-0 mr-0 pl-0 pr-0">
            <b-progress
              :max="imageUrls.length"
              animated
              variant="success"
              height="1.5em"
            >
              <b-progress-bar :value="current_img_idx + 1">
                <strong class="text-dark">
                  Progress: {{ current_img_idx + 1 }} / {{ imageUrls.length }}
                </strong>
              </b-progress-bar>
            </b-progress>
          </b-col>
        </b-row>

        <!-- IMAGE CONTAINER -->
        <b-row class="align-items-center text-center mt-2 mb-2">
          <b-col class="d-flex flex-column align-items-center">
            <b-link href="#">
              <b-img
                :id="`tn-img-${current_img_idx}`"
                v-b-modal="`modal-${imageUrls[current_img_idx]}`"
                rounded
                :src="imageUrls[current_img_idx]"
                class="border border-dark shadow shadow-lg"
                style="max-height: 400px"
              />
              <b-tooltip
                :target="`tn-img-${current_img_idx}`"
                placement="top"
                triggers="hover"
                noninteractive
              >
                Click to enlarge
              </b-tooltip>
            </b-link>
          </b-col>
          <!-- ENLARGE MODAL -->
          <b-modal
            :id="`modal-${imageUrls[current_img_idx]}`"
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
              :src="imageUrls[current_img_idx]"
              style="max-height: 60vh"
            />
            <template #modal-footer>
              <b-container fluid class="text-left m-0 p-0">
                <b-row class="m-0 p-0 no-gutters border-bottom border-dark">
                  <b-col
                    md="2"
                    class="font-weight-bold border-right border-dark"
                  >
                    Caption:
                  </b-col>
                  <b-col md="10" class="font-italic">{{
                    sample.caption
                  }}</b-col>
                </b-row>
                <b-row class="m-0 p-0 no-gutters">
                  <b-col
                    md="2"
                    class="font-weight-bold border-right border-dark"
                  >
                    Focus Word:
                  </b-col>
                  <b-col md="10" class="font-italic">{{ sample.focus }}</b-col>
                </b-row>
              </b-container>
            </template>
          </b-modal>
        </b-row>
      </b-container>

      <!-- RATING -->
      <b-container fluid class="border border-dark rounded-bottom bg-info">
        <!-- CONTEXT -->
        <b-row>
          <b-col
            md="3"
            class="d-flex flex-column align-items-center justify-content-center border-right border-dark"
          >
            <p>How well does the caption match the image?</p>
          </b-col>
          <b-col
            md="2"
            class="d-flex flex-column align-items-center border-right border-dark"
          >
            <star-rating
              v-model="contextRatings[current_img_idx]"
              class="d-flex pt-1"
              :increment="sample.rating_step"
              :show-rating="false"
              :border-width="1"
              :star-size="starSize"
              border-color="#000"
              active-color="#FFC107"
              inactive-color="#FFF"
              @rating-selected="setRating('context', $event, current_img_idx)"
            ></star-rating>
            <div class="d-flex pt-1">
              <label for="`contextNotRelevantCheckBox_{current_img_idx}`">
                Not matching at all&nbsp;
              </label>
              <b-form-checkbox
                :id="`contextNotRelevantCheckBox_${current_img_idx}`"
                v-model="contextNotRelevant[current_img_idx]"
                @input="setNotRelevant('context', $event, current_img_idx)"
              ></b-form-checkbox>
            </div>
          </b-col>
          <b-col md="7" class="overflow-auto" style="max-height: 100px">
            <h5 class="p-1 font-italic">
              {{ sample.caption }}
            </h5>
          </b-col>
        </b-row>

        <!-- FOCUS -->
        <b-row class="border-top border-dark">
          <b-col
            md="3"
            class="d-flex flex-column align-items-center justify-content-center border-right border-dark"
          >
            <p>
              How well does the focus word match the highlighted region in the
              image?
            </p>
          </b-col>
          <b-col
            md="2"
            class="d-flex flex-column align-items-center border-right border-dark"
          >
            <star-rating
              v-model="focusRatings[current_img_idx]"
              class="d-flex pt-1"
              :increment="sample.rating_step"
              :show-rating="false"
              :border-width="1"
              :star-size="starSize"
              border-color="#000"
              active-color="#FFC107"
              inactive-color="#FFF"
              @rating-selected="setRating('focus', $event, current_img_idx)"
            ></star-rating>
            <div class="d-flex pt-1">
              <label for="`focusNotRelevantCheckBox_{current_img_idx}`">
                Not matching at all&nbsp;
              </label>
              <b-form-checkbox
                :id="`focusNotRelevantCheckBox_${current_img_idx}`"
                v-model="focusNotRelevant[current_img_idx]"
                @input="setNotRelevant('focus', $event, current_img_idx)"
              ></b-form-checkbox>
            </div>
          </b-col>
          <b-col md="7"
            ><h5
              class="p-1 font-italic"
              style="max-height: 200px; overflow-y: auto"
            >
              {{ sample.focus }}
            </h5></b-col
          >
        </b-row>
      </b-container>

      <!-- NEXT / PREV BUTTON -->
      <b-row class="text-center no-gutters">
        <b-col v-if="current_img_idx < imageUrls.length - 1">
          <b-button
            variant="success"
            block
            squared
            size="small"
            @click="current_img_idx += 1"
          >
            Next Image
          </b-button>
        </b-col>

        <b-col v-if="current_img_idx > 0">
          <b-button
            variant="danger"
            block
            squared
            size="small"
            @click="current_img_idx -= 1"
          >
            Previous Image
          </b-button>
        </b-col>
      </b-row>

      <!-- FORM FOOTER BUTTONS -->
      <b-container id="imageRankingFooter" fluid class="p-1 fixed-bottom">
        <b-form-row class="m-0 text-center">
          <h3 v-if="hitPreview" class="text-warning bg-dark w-100">
            You must accept this HIT before working on it!
          </h3>
          <b-button-group v-else class="w-100 mt-1 mb-1">
            <!--  SUBMIT BUTTON   -->
            <b-button
              type="submit"
              variant="primary"
              :disabled="submitDisabled"
            >
              <div v-if="submitDisabled" class="w-100">
                Please rate every image!
              </div>
              <span v-else>Submit Answer</span>
            </b-button>
            <!--  LOAD NEXT SAMPLE BUTTON   -->
            <b-button
              v-if="rsId === ''"
              type="button"
              variant="warning"
              @click="loadNextSample"
            >
              Get New Sample
            </b-button>
            <!--  FEEDBACK BUTTON   -->
            <b-button v-b-modal.feedbackModal variant="info">
              Provide Feedback
            </b-button>
          </b-button-group>
        </b-form-row>
      </b-container>
    </b-form>

    <!--  FEEDBACK MODAL   -->
    <b-modal
      id="feedbackModal"
      title="Any comments, criticism or thoughts?"
      hide-footer
    >
      <FeedbackForm :worker-id="workerId" :sample-id="rsId" :hit-id="hitId" />
    </b-modal>

    <!--  HIDDEN MTURK FORM   -->
    <form id="hiddenMTurkForm" method="post" :action="mturkExternalSubmitUrl">
      <input
        id="assignmentId"
        type="hidden"
        name="assignmentId"
        :value="assignmentId"
      />
      <input id="rrId" type="hidden" name="rrId" :value="rrIdString" />
      <input id="ratings" type="hidden" name="ratings" :value="ratingsString" />
    </form>
  </b-container>
</template>

<script>
import FeedbackForm from '~/components/FeedbackForm'

export default {
  name: 'RatingForm',
  components: { FeedbackForm },
  props: {
    rsId: {
      type: String,
      default: '',
    },
    assignmentId: {
      type: String,
      default: '',
    },
    workerId: {
      type: String,
      default: '',
    },
    hitId: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      starSize: 20,
      imageUrls: [],
      contextRatings: [],
      focusRatings: [],
      contextNotRelevant: [],
      focusNotRelevant: [],
      initRatingValue: -1312,
      sample: null,
      loading: true,
      submitSuccess: false,
      submitError: false,
      loadSuccess: false,
      loadError: false,
      rrId: '',
      sample_cooldown: 0, // waiting time until next sample,
      current_img_idx: 0,
    }
  },
  computed: {
    submitDisabled() {
      return (
        this.contextRatings.includes(this.initRatingValue) ||
        this.focusRatings.includes(this.initRatingValue) ||
        (this.currentUser === null && this.workerId === '')
      )
    },
    hitPreview() {
      return this.assignmentId === 'ASSIGNMENT_ID_NOT_AVAILABLE'
    },
    rrIdString() {
      return JSON.stringify(this.rrId)
    },
    ratingsString() {
      return JSON.stringify(this.ratings)
    },
    mturkExternalSubmitUrl() {
      let sub = ''
      if (
        this.$config.mturkSandbox === true ||
        this.$config.mturkSandbox === 'True' ||
        this.$config.mturkSandbox === 'true' ||
        this.$config.mturkSandbox === '1'
      ) {
        sub = 'workersandbox'
      } else sub = 'www'

      return `https://${sub}.mturk.com/mturk/externalSubmit`
    },
    currentUser() {
      return this.$store.state.current_user.currentUser
    },
    currentUserId() {
      return this.currentUser === null
        ? ''
        : JSON.stringify(this.currentUser.userId).replaceAll('"', '')
    },
    currentUserJwt() {
      return this.currentUser === null
        ? ''
        : JSON.stringify(this.currentUser.jwt).replaceAll('"', '')
    },
  },
  created() {
    // set the app header text
    const headerText = `How well do the <strong> caption </strong> and <strong> focus word </strong> match? Please rate each image!`
    this.$nuxt.$emit('set-app-header-text', headerText)

    // load the sample
    if (this.rsId === '') this.loadNextSample()
    else this.loadSample()

    // cooldown function if we have to wait for the next sample
    const self = this
    setInterval(function () {
      if (self.sample_cooldown > 0) {
        self.sample_cooldown--
        if (self.sample_cooldown === 0) {
          self.loadNextSample()
        }
      }
    }, 1000)
  },
  mounted() {
    this.$nextTick(function () {
      this.calcStarSize()
    })
    window.addEventListener('resize', this.calcStarSize)
  },
  methods: {
    calcStarSize() {
      this.starSize = (window.innerWidth / 100) * 2
    },
    getImageIds(urls) {
      return this.$imageApiClient.getIds(urls)
    },
    resetDataBeforeLoadingSample() {
      // reset flags
      this.loading = true
      this.loadError = false
      this.loadSuccess = false
      this.submitError = false
      this.submitSuccess = false

      // reset rating data
      this.contextRatings = []
      this.focusRatings = []
    },
    setNotRelevant(ctx, notRel, idx) {
      if (ctx === 'context') {
        if (typeof notRel === 'boolean') {
          // we have to use $set here because single array item assignments are not reactive
          if (notRel) {
            this.$set(this.contextRatings, idx, 0.0)
          } else {
            this.$set(this.contextRatings, idx, this.initRatingValue)
          }
          this.$set(this.contextNotRelevant, idx, notRel)
        }
      } else if (ctx === 'focus') {
        if (typeof notRel === 'boolean') {
          // we have to use $set here because single array item assignments are not reactive
          if (notRel) {
            this.$set(this.focusRatings, idx, 0.0)
          } else {
            this.$set(this.focusRatings, idx, this.initRatingValue)
          }
          this.$set(this.focusNotRelevant, idx, notRel)
        }
      }
    },
    setRating(ctx, rating, idx) {
      // we have to use $set here because single array item assignments are not reactive
      if (ctx === 'context') {
        this.$set(this.contextNotRelevant, idx, false)
        this.$set(this.contextRatings, idx, rating)
      } else if (ctx === 'focus') {
        this.$set(this.focusNotRelevant, idx, false)
        this.$set(this.focusRatings, idx, rating)
      }
    },
    async onSubmit(event = null) {
      if (event !== null) event.preventDefault()
      this.loading = true
      this.submitError = false
      this.submitSuccess = false

      // submit to own API
      this.rrId = await this.$resultApiClient.submitRatingWithFocusResult(
        this.sample.id,
        this.contextRatings,
        this.focusRatings,
        this.workerId,
        this.assignmentId,
        this.hitId,
        this.currentUserId,
        this.currentUserJwt
      )
      this.submitSuccess =
        this.rrId !== '' && this.rrId !== undefined && this.rrId !== null
      this.submitError = !this.submitSuccess

      // submit to MTurk if in MTurk mode
      if (this.submitSuccess && this.assignmentId !== '') {
        // via axios
        // fixme currently not working because we would have to follow the redirect and set the cookie correctly
        // fixme see the last comment (from AWS staff) https://forums.aws.amazon.com/thread.jspa?messageID=553442
        // fixme we COULD get this working but it would be PITA
        //   this.submitSuccess = await this.$mturkSubmitService.submitAssignment(
        //     ids,
        //     this.assignmentId,
        //     this.rrId
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
    async initData() {
      // load image urls
      this.imageUrls = await this.$imageApiClient.getUrls(
        this.sample.image_ids,
        false
      )
      this.contextRatings = []
      this.focusRatings = []
      this.current_img_idx = 0

      this.sample.image_ids.forEach((i) => {
        this.contextRatings.push(this.initRatingValue)
        this.focusRatings.push(this.initRatingValue)
      })

      this.contextNotRelevant = []
      this.focusNotRelevant = []
      this.sample.image_ids.forEach((i) => {
        this.contextNotRelevant.push(false)
        this.focusNotRelevant.push(false)
      })

      this.$nuxt.$emit('study-progress-changed')
    },
    async loadNextSample() {
      this.resetDataBeforeLoadingSample()

      const resp = await this.$sampleApiClient.nextRatingWithFocusSample()
      // check if it's a sample or an int that expresses the waiting time in seconds until the next sample is available
      if (Number.isInteger(resp)) {
        this.sample_cooldown = resp
      } else {
        this.sample = resp
        this.loadSuccess = this.sample !== null
        this.loadError = !this.loadSuccess

        if (this.loadSuccess) {
          await this.initData()
        }
      }
      this.loading = false
    },
    async loadSample() {
      this.resetDataBeforeLoadingSample()

      this.sample = await this.$sampleApiClient.loadRatingWithFocusSample(
        this.rsId
      )
      this.loadSuccess = this.sample !== null
      this.loadError = !this.loadSuccess

      if (this.loadSuccess) {
        await this.initData()
      }

      this.loading = false

      this.$nuxt.$emit('study-progress-changed')
    },
  },
}
</script>

<style scoped></style>
