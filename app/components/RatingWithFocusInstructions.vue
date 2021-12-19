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
      screen size of 1280x1050 pixels with no browser zoom enabled.
    </b-alert>
    <b-container fluid class="text-center">
      <b-form-checkbox
        v-model="ratingWithFocusInstructionsRead"
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
          <div style="font-size: 1.2rem">
            To complete the task, you are shown five images.
            <br />
            Then, for each of the images you have to
            <ul>
              <li>
                <strong> rate how well the caption matches the image</strong>
              </li>
              <li>
                <strong>
                  rate how well the focus word matches the highlighted region in
                  the image
                </strong>
              </li>
            </ul>
            on a 5-star scale.

            <br />
            <br />
            The <strong class="text-danger">caption</strong> is shown in the
            <strong class="text-danger">first</strong> row of the
            <span class="bg-info rounded p-1">green-ish box</span>
            below the image.
            <br />
            The <strong class="text-danger">focus word</strong> is shown in the
            <strong class="text-danger">second</strong> row of the
            <span class="bg-info rounded p-1">green-ish box</span>
            below the image.
            <br />
            <br />
            <strong>
              Although a perfect match between the sentences or the focus-words
              with the highlighted-image region or the entire image are desired,
              it does not always need to be an exact match.
            </strong>
            <br />
            <br />
            Once you've rated every image, the submit button gets enabled.
          </div>
        </section>
      </b-row>

      <!--      <b-row class="mb-2">-->
      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h3 class="text-monospace">
              <u style="text-decoration-style: dashed"> Enlarge an image </u>
            </h3>
          </header>
          <p>
            To enlarge and image, simply
            <strong> click on the respective image </strong>
            and a modal with with the enlarged image will show up.
          </p>
        </section>
      </b-row>

      <b-row class="mb-2 mt-2">
        <b-button block variant="success" @click="onSubmit">
          Ok, I got it! Let's start!
        </b-button>
        <b-form-checkbox
          v-model="ratingWithFocusInstructionsRead"
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
  name: 'RatingWithFocusInstructions',
  emits: ['rating-with-focus-instructions-read'],
  data() {
    return {
      ratingWithFocusInstructionsRead: false,
    }
  },
  watch: {
    ratingWithFocusInstructionsRead(read) {
      localStorage.setItem('ratingWithFocusInstructionsRead', read)
      this.ratingWithFocusInstructionsRead = read
    },
  },
  mounted() {
    this.ratingWithFocusInstructionsRead = JSON.parse(
      localStorage.getItem('ratingWithFocusInstructionsRead')
    )
    if (this.ratingWithFocusInstructionsRead === true) {
      this.$nextTick(() => {
        this.$emit('rating-with-focus-instructions-read')
      })
    }
  },
  created() {
    if (
      process.browser &&
      localStorage.getItem('ratingWithFocusInstructionsRead') === null
    )
      localStorage.setItem('ratingWithFocusInstructionsRead', 'false')
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$emit('rating-with-focus-instructions-read')
    },
  },
}
</script>

<style scoped></style>
