<template>
  <b-jumbotron
    fluid
    header="Welcome!"
    lead="Please read the instructions or watch the instructions video(s) to make sure you know what to do before you start!"
    class="rounded my-auto"
  >
    <b-container fluid class="text-center">
      <b-form-checkbox
        v-model="readBefore"
        name="show-next-time-checkbox"
        class="text-left"
        switch
      >
        Show instructions next time
      </b-form-checkbox>
      <b-row class="mb-2">
        <section class="w-100 p-2 text-left">
          <header>
            <h2 class="text-monospace">
              <u style="text-decoration-style: dashed"> Goal of the task </u>
            </h2>
          </header>
          <p>
            To complete the task, you have to
            <strong>
              rank at least your top {{ $nuxt.$config.minNumRanks }} images and
              tag all remaining images as irrelevant
            </strong>
            regarding a given caption in the green-ish box below the
            image-selection area in the middle part of the application. Your
            progress is highlighted by a progress bar in the bottom part of the
            application. Once you've processed every image, the submit button
            becomes available.
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
              src="https://www.youtube-nocookie.com/embed/RGYN5OW_c2c"
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
                Tag an image as irrelevant
              </u>
            </h3>
          </header>
          <p>
            To tag an image as irrelevant,
            <strong>
              simply right-click it in the image-selection area in the center of
              the application.
            </strong>
            An image is tagged as irrelevant if a red x-overlay appears on the
            respective image in the image-selection area.
          </p>
          <b-button
            v-b-toggle="'tag-irrelevant-video'"
            variant="primary"
            size="sm"
          >
            Toggle Example
          </b-button>

          <b-collapse
            id="tag-irrelevant-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com/embed/RgJzTmvjg_A"
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
              src="https://www.youtube-nocookie.com//embed/E6wgS4rEZiM"
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
                Remove the irrelevant tag of an image
              </u>
            </h3>
          </header>
          <p>
            To remove the irrelevant tag of an image,
            <strong>
              (left or right) click on the red x-overlay in the image-selection
              area.
            </strong>
            You can see, that the red x-overlay of the respective image has
            disappeared.
          </p>
          <b-button
            v-b-toggle="'remove-irrelevant-video'"
            variant="primary"
            size="sm"
          >
            Toggle Example
          </b-button>

          <b-collapse
            id="remove-irrelevant-video"
            class="pt-1 border border-dark rounded-bottom w-100 text-center"
          >
            <iframe
              width="800"
              height="450"
              src="https://www.youtube-nocookie.com//embed/Bb8TvK48wBc"
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
              src="https://www.youtube-nocookie.com/embed/dhHQR_WAEnc"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </b-collapse>
        </section>
      </b-row>

      <b-row class="mb-2">
        <b-button v-b-toggle="'full-video'" class="w-100" variant="primary">
          Full tutorial video (1:40 min)
        </b-button>

        <b-collapse
          id="full-video"
          class="pt-1 border border-dark rounded-bottom w-100 text-center"
        >
          <iframe
            width="800"
            height="450"
            src="https://www.youtube-nocookie.com/embed/SqV9ta6DNi8?controls=0&vq=hd720"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </b-collapse>
      </b-row>

      <b-row class="mb-2 mt-2">
        <b-button block variant="success" @click="onSubmit">
          Ok, I got it! Let's start!
        </b-button>
        <b-form-checkbox
          v-model="readBefore"
          name="show-next-time-checkbox"
          switch
        >
          Show instructions next time
        </b-form-checkbox>
      </b-row>
    </b-container>
  </b-jumbotron>
</template>

<script>
export default {
  name: 'Instructions',
  emits: ['instructions-read'],
  data() {
    return {
      readBefore: true,
    }
  },
  watch: {
    readBefore(show) {
      localStorage.setItem('readBefore', show)
    },
  },
  mounted() {
    this.readBefore = JSON.parse(localStorage.getItem('readBefore'))
    if (this.readBefore === false) {
      this.$nextTick(() => {
        this.$emit('instructions-read')
      })
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$emit('instructions-read')
    },
  },
}
</script>

<style scoped></style>
