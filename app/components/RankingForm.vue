<template>
  <b-container fluid>
    <b-form @submit="onSubmit" @reset="onReset">
      <!-- IMAGE POOL -->
      <b-container>
        <Draggable
          :value="images"
          :group="{ name: 'images', pull: 'clone', put: false, sort: false }"
          class="row text-center no-gutters"
        >
          <b-col v-for="imgUrl in images" :key="imgUrl" lg="2" md="2" sm="3">
            <b-img
              :id="`img-${imgUrl}`"
              thumbnail
              fluid
              :src="imgUrl"
              height="130px"
              width="130px"
            />
            <b-popover
              :target="`img-${imgUrl}`"
              triggers="hover"
              placement="bottom"
            >
              <b-img fluid :src="imgUrl" />
            </b-popover>
          </b-col>
        </Draggable>
      </b-container>

      <!-- IMAGE RANKING -->
      <b-container fluid>
        <Draggable
          :list="rankedImages"
          :group="{ name: 'images', put: ranksNotFull }"
          tag="div"
          class="d-flex flex-row justify-content-center mt-1 bg-light ranks h-100 flex-wrap"
          @add="addToRankedImages"
        >
          <h1 v-if="showDragabbleHint" class="text-dark my-auto">
            Drag n' Drop Images Here To Rank
          </h1>

          <div v-for="(imgUrl, idx) in rankedImages" v-else :key="idx">
            <b-avatar
              :id="`ranked-${imgUrl}`"
              rounded="sm"
              :src="imgUrl"
              :badge="`${idx + 1}`"
              size="130px"
              badge-top
              class="ml-1"
            />
            <b-popover
              :target="`ranked-${imgUrl}`"
              triggers="hover"
              placement="top"
            >
              <b-img fluid :src="imgUrl" />
            </b-popover>
          </div>
        </Draggable>

        <b-progress
          :max="numRanks"
          show-progress
          variant="success"
          class="mt-1"
        >
          <b-progress-bar :value="numRankedImages">
            <span>
              Progress:<strong>{{ numRankedImages }} / {{ numRanks }}</strong>
            </span>
          </b-progress-bar>
        </b-progress>
      </b-container>

      <b-form-row>
        <b-button-group class="w-100 mt-3">
          <b-button type="submit" variant="primary" :disabled="ranksNotFull">
            <span v-if="ranksNotFull">
              What image is best described by the query? Please rank the Top-10!
            </span>
            <span v-else>Submit your ranking</span>
          </b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form-row>
    </b-form>
  </b-container>
</template>

<script>
// import _ from 'lodash'

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
  },
  data() {
    return {
      rankedImages: [],
      images: this.randomImages(this.numImages),
      numRankedImages: 0,
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
  methods: {
    randomImages(n) {
      const res = []
      let i
      for (i = 0; i < n; i++) {
        res.push(`https://picsum.photos/id/${i + 20}/250/250`)
      }
      // return _.shuffle(res)
      return res
    },
    addToRankedImages(evt) {
      // remove duplicates
      // https://stackoverflow.com/questions/9229645/remove-duplicate-values-from-js-array
      const lenBefore = this.rankedImages.length
      this.rankedImages = [...new Set(this.rankedImages)]
      const itemAdded =
        this.rankedImages.length === lenBefore + 1 ||
        this.rankedImages.length === lenBefore
      if (itemAdded) {
        this.incProgress()
      }
    },
    incProgress(n = 1) {
      this.numRankedImages += n
    },
    decProgress(n = 1) {
      this.numRankedImages -= n
    },
    onSubmit(event) {
      event.preventDefault()
      alert(JSON.stringify(this.rankedImages))
    },
    onReset(event) {
      event.preventDefault()
      this.rankedImages = []
      alert(JSON.stringify(this.rankedImages))
    },
  },
}
</script>

<style scoped>
.ranks {
  min-height: 130px;
}
</style>
