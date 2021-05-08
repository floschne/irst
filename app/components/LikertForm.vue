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
      <b-button v-if="lsId === ''" variant="primary" @click="loadNextSample">
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
      <b-button v-if="lsId === ''" variant="primary" @click="loadNextSample"
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
      <b-button v-if="lsId === ''" variant="primary" @click="loadNextSample">
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

    <!--  LIKERT FORM   -->
    <b-form
      v-else-if="!loading && loadSuccess && !loadError"
      @submit="onSubmit"
    >
      <!-- Image Container -->
      <b-container
        fluid
        style="max-height: 550px"
        class="overflow-auto border border-dark rounded-top bg-secondary p-1"
      >
        <b-row
          class="text-center no-gutters d-flex flex-row justify-content-around align-items-center"
        >
          <!-- SINGLE IMAGE CONTAINER -->
          <b-col
            v-for="(tnUrl, idx) in thumbnailUrls"
            :key="`tn-col-${idx}`"
            class="mt-1 d-flex justify-content-center"
            lg="1"
            md="2"
            sm="3"
            :style="`min-width: ${img_size}rem; min-height: ${img_size}rem`"
          >
            <b-link href="#" class="image-container image-size">
              <b-img
                :id="`tn-img-${idx}`"
                v-b-modal="`modal-${tnUrl}`"
                thumbnail
                rounded
                :src="tnUrl"
                class="image-size"
              />
              <b-tooltip
                :target="`tn-img-${idx}`"
                placement="top"
                triggers="hover"
                noninteractive
              >
                Click to enlarge
              </b-tooltip>
            </b-link>

            <!-- ENLARGE MODAL -->
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
                <p>{{ sample.caption }}</p>
              </template>
            </b-modal>
          </b-col>
        </b-row>
      </b-container>

      <!-- CAPTION -->
      <h5
        class="p-1 border border-dark rounded-bottom bg-info font-italic text-center"
        style="max-height: 200px; overflow-y: auto"
      >
        {{ sample.caption }}
      </h5>

      <b-container id="imageRankingFooter" fluid class="p-1 fixed-bottom">
        <b-container
          fluid
          class="d-flex flex-row justify-content-center align-items-center mt-1 bg-light border border-dark h-100 rounded"
          :style="`min-height: ${img_size}rem;
           max-height: ${img_size + 1}rem; max-width: 100vw`"
        >
          <b-form-group :label="sample.question" label-size="lg">
            <b-form-radio-group
              id="answerSelection"
              v-model="chosenAnswer"
              :options="sampleAnswers"
              name="answerSelection"
              size="large"
              buttons
              button-variant="outline-primary"
            ></b-form-radio-group>
          </b-form-group>
        </b-container>

        <!-- FORM BUTTONS -->
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
                Please choose your answer!
              </div>
              <span v-else>Submit Answer</span>
            </b-button>
            <!--  LOAD NEXT SAMPLE BUTTON   -->
            <b-button
              v-if="lsId === ''"
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
      <FeedbackForm :worker-id="workerId" :sample-id="lsId" :hit-id="hitId" />
    </b-modal>

    <!--  HIDDEN MTURK FORM   -->
    <form id="hiddenMTurkForm" method="post" :action="mturkExternalSubmitUrl">
      <input
        id="assignmentId"
        type="hidden"
        name="assignmentId"
        :value="assignmentId"
      />
      <input id="lrId" type="hidden" name="lrId" :value="lrIdString" />
      <input
        id="chosenAnswer"
        type="hidden"
        name="chosenAnswer"
        :value="chosenAnswerString"
      />
    </form>
  </b-container>
</template>

<script>
import FeedbackForm from '~/components/FeedbackForm'

export default {
  name: 'LikertForm',
  components: { FeedbackForm },
  props: {
    lsId: {
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
      imageUrls: [],
      thumbnailUrls: [],
      chosenAnswer: '',
      sample: null,
      sampleAnswers: null,
      loading: true,
      submitSuccess: false,
      submitError: false,
      loadSuccess: false,
      loadError: false,
      img_size: 10,
      lrId: '',
      sample_cooldown: 0, // waiting time until next sample,
    }
  },
  computed: {
    submitDisabled() {
      return this.chosenAnswer === '' || this.chosenAnswer === null
    },
    hitPreview() {
      return this.assignmentId === 'ASSIGNMENT_ID_NOT_AVAILABLE'
    },
    chosenAnswerString() {
      return JSON.stringify(this.chosenAnswer)
    },
    lrIdString() {
      return JSON.stringify(this.lrId)
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
  },
  created() {
    if (this.lsId === '') this.loadNextSample()
    else this.loadSample()

    const self = this
    // cooldown function if we have to wait for the next sample
    setInterval(function () {
      if (self.sample_cooldown > 0) {
        self.sample_cooldown--
        if (self.sample_cooldown === 0) {
          self.loadNextSample()
        }
      }
    }, 1000)
  },
  methods: {
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

      // reset answer data
      this.chosenAnswer = ''
      this.sampleAnswers = []
    },
    async onSubmit(event = null) {
      if (event !== null) event.preventDefault()
      this.loading = true
      this.submitError = false
      this.submitSuccess = false

      // submit to own API
      this.lrId = await this.$resultApiClient.submitLikertResult(
        this.sample.id,
        this.chosenAnswer,
        this.workerId,
        this.assignmentId,
        this.hitId
      )
      this.submitSuccess =
        this.lrId !== '' && this.lrId !== undefined && this.lrId !== null
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
        //     this.lrId
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
      // load thumbnail urls
      this.thumbnailUrls = await this.$imageApiClient.getUrls(
        this.sample.image_ids,
        true
      )
      // build sampleAnswers for answerSelection radio group
      const sampleAnswers = []
      this.sample.answers.forEach((answer) => {
        sampleAnswers.push({ text: answer, value: answer })
      })
      this.sampleAnswers = sampleAnswers

      this.$nuxt.$emit('study-progress-changed')
    },
    async loadNextSample() {
      this.resetDataBeforeLoadingSample()

      const resp = await this.$sampleApiClient.nextLikertSample()
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

      this.sample = await this.$sampleApiClient.loadLikertSample(this.lsId)
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

<style scoped>
.image-size {
  min-height: 10rem !important;
  max-height: 10rem !important;
  min-width: 10rem !important;
  max-width: 10rem !important;
}

.image-container {
  position: relative;
  text-align: center;
  width: 100%;
}
</style>
