<template>
  <b-jumbotron
    fluid
    header="Welcome!"
    lead="Please read the instructions or watch the instructions videos to make sure you know what to do before you start!"
    class="rounded my-auto"
  >
    <b-alert show dismissible fade variant="warning" class="border border-dark">
      <b-icon font-scale="1.5" icon="exclamation-triangle" />
      &nbsp;This app does not support mobile devices and requires a minimum
      screen size of 900x800 pixels with no browser zoom enabled.
    </b-alert>
    <b-container fluid class="text-center">
      <b-form-checkbox
        v-model="rankingInstructionsRead"
        name="show-next-time-checkbox"
        class="text-left"
        switch
      >
        Hide instructions next time
      </b-form-checkbox>
      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h1 class="text-monospace">
              <u style="text-decoration-style: dashed"> Goal of the task </u>
            </h1>
          </header>
          <p style="font-size: 1.2rem">
            To complete the task, you have to
            <strong>
              rank at least your top {{ $nuxt.$config.minNumRanks }} images
            </strong>
            regarding a given caption in the
            <span class="bg-info rounded p-1">green-ish box</span> below the
            image-selection area in the middle part of the application.
            <br />
            <strong>
              Note that the images
              <u style="text-decoration-style: solid">
                do not have to match exactly
              </u>
              but should just be related to the caption.
            </strong>
            <br />
            For example, if the caption is about specific a person, all images
            with persons are regarded as being related.
            <br />
            Once you've ranked your top image, the submit button gets enabled.
          </p>
        </section>
      </b-row>

      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h3 class="text-monospace">
              <u style="text-decoration-style: dashed">Ranking an image</u>
            </h3>
          </header>
          <p>
            To rank an image,
            <strong>
              simply drag and drop it into the ranking area at the bottom part
              of the application.
            </strong>
            An image is ranked if a green checkmark-overlay appears on the
            respective image in the image-selection area. The rank of the image
            is indicated by the number in the blue badge in the top-right corner
            of the respective image in the ranking area.
          </p>
          <b-button v-b-toggle="'ranking-video'" variant="primary" size="sm">
            Toggle Example
          </b-button>

          <b-collapse
            id="ranking-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/6GtOt7uLhyg"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </b-collapse>
        </section>
      </b-row>

      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h3 class="text-monospace">
              <u style="text-decoration-style: dashed">
                Change the ranking of an image
              </u>
            </h3>
          </header>
          <p>
            To change the ranking of an image,
            <strong>
              drag and drop it to the preferred position in the ranking area in
              the bottom part of the application.
            </strong>
            You can see, that the rank of the image, shown in the blue badge,
            changed according to the new position.
          </p>
          <b-button
            v-b-toggle="'change-ranking-video'"
            variant="primary"
            size="sm"
          >
            Toggle Example
          </b-button>

          <b-collapse
            id="change-ranking-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/l1Bu5yxAQDY"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </b-collapse>
        </section>
      </b-row>

      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <h3 class="text-monospace">
            <u style="text-decoration-style: dashed"> Remove a ranked image </u>
          </h3>
          <p>
            To remove a ranked image,
            <strong>
              click on the green checkmark overlay in the image-selection area
              or right-click it in the ranking area.
            </strong>
            You can see, that the green checkmark-overlay in the image-selection
            area has disappeared.
          </p>
          <b-button
            v-b-toggle="'remove-ranked-video'"
            variant="primary"
            size="sm"
          >
            Toggle Example
          </b-button>

          <b-collapse
            id="remove-ranked-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/Oc0dN7C7yuI"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </b-collapse>
        </section>
      </b-row>

      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h3 class="text-monospace">
              <u style="text-decoration-style: dashed"> Enlarge an image </u>
            </h3>
          </header>
          <p>
            To enlarge and image,
            <strong>
              (left-)click on the respective image if it has neither the green
              checkmark-overlay nor the red x-overlay in the image-selection
              area OR (left-)click an image in the ranking area.
            </strong>
          </p>
          <b-button v-b-toggle="'enlarge-video'" variant="primary" size="sm">
            Toggle Example
          </b-button>

          <b-collapse
            id="enlarge-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/nErYZd4T7R4"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </b-collapse>
        </section>
      </b-row>

      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h3 class="text-monospace">
              <u style="text-decoration-style: dashed">Providing Feedback</u>
            </h3>
          </header>
          <p>
            If you have any comments or criticism you can provide your feedback
            by
            <strong>clicking on the</strong>
            <span class="bg-info rounded p-1">'Provide Feedback'-button</span>
            on the bottom of the application.
            <br />
            If you want to provide anonymous feedback, make your to set the
            respective switch.
          </p>
          <b-button v-b-toggle="'provide-feedback'" variant="primary" size="sm">
            Toggle Example
          </b-button>

          <b-collapse
            id="provide-feedback"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/22ZXs1ztCBo"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </b-collapse>
        </section>
      </b-row>

      <b-row class="mb-2 mt-2">
        <b-button block variant="success" @click="onSubmit">
          Ok, I got it! Let's start!
        </b-button>
        <b-form-checkbox
          v-model="rankingInstructionsRead"
          name="show-next-time-checkbox"
          switch
        >
          Hide instructions next time
        </b-form-checkbox>
      </b-row>
    </b-container>
  </b-jumbotron>
</template>

<script>
export default {
  name: 'RankingInstructions',
  emits: ['ranking-instructions-read'],
  data() {
    return {
      rankingInstructionsRead: false,
    }
  },
  watch: {
    rankingInstructionsRead(read) {
      localStorage.setItem('rankingInstructionsRead', read)
      this.rankingInstructionsRead = read
    },
  },
  mounted() {
    this.rankingInstructionsRead = JSON.parse(
      localStorage.getItem('rankingInstructionsRead')
    )
    if (this.rankingInstructionsRead === true) {
      this.$nextTick(() => {
        this.$emit('ranking-instructions-read')
      })
    }
  },
  created() {
    if (
      process.browser &&
      localStorage.getItem('rankingInstructionsRead') === null
    )
      localStorage.setItem('rankingInstructionsRead', 'false')
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$emit('ranking-instructions-read')
    },
  },
}
</script>

<style scoped></style>
