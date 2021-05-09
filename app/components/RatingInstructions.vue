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
        v-model="ratingInstructionsRead"
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
            <strong> rate each of the images </strong>
            on a 5-star scale according to the caption in the
            <span class="bg-info rounded p-1">green-ish box</span> below the
            images.
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
            Once you've rated every image, the submit button gets enabled.
          </p>
        </section>
      </b-row>

      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h3 class="text-monospace">
              <u style="text-decoration-style: dashed">Rating an image</u>
            </h3>
          </header>
          <p>
            To rate an image just select the number of stars with your cursor.
          </p>
          <p>
            If an images is not related at all, i.e., you want
            <strong>
              to assign zero stars, please select the checkbox below the rating </strong
            >.
          </p>
          <p>
            <strong>5 stars means that the image is perfectly related</strong>
            to the caption in the
            <span class="bg-info rounded p-1">green-ish box</span> below the
            images.
          </p>
          <p>
            <strong>0 stars means that the image is not related</strong>
            to the caption at all.
          </p>
          <b-button v-b-toggle="'rating-video'" variant="primary" size="sm">
            Toggle Example
          </b-button>

          <b-collapse
            id="rating-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/fMimZvy3qV4"
              title="YouTube video player"
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
          v-model="ratingInstructionsRead"
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
  name: 'RatingInstructions',
  emits: ['rating-instructions-read'],
  data() {
    return {
      ratingInstructionsRead: false,
    }
  },
  watch: {
    ratingInstructionsRead(read) {
      localStorage.setItem('ratingInstructionsRead', read)
      this.ratingInstructionsRead = read
    },
  },
  mounted() {
    this.ratingInstructionsRead = JSON.parse(
      localStorage.getItem('ratingInstructionsRead')
    )
    if (this.ratingInstructionsRead === true) {
      this.$nextTick(() => {
        this.$emit('rating-instructions-read')
      })
    }
  },
  created() {
    if (
      process.browser &&
      localStorage.getItem('ratingInstructionsRead') === null
    )
      localStorage.setItem('ratingInstructionsRead', 'false')
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$emit('rating-instructions-read')
    },
  },
}
</script>

<style scoped></style>
