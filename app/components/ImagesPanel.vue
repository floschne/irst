<template>
  <b-container fluid>
    <b-container>
      <Draggable
        :value="images"
        :group="{ name: 'images', pull: 'clone', put: false, sort: false }"
        class="row text-center no-gutters"
      >
        <b-col v-for="imgUrl in images" :key="imgUrl" md="3">
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
            triggers="hover focus"
            placement="bottom"
          >
            <b-img fluid :src="imgUrl" />
          </b-popover>
        </b-col>
      </Draggable>
    </b-container>

    <Draggable
      :list="rankedImages"
      :group="{ name: 'images', put: ranksFull }"
      tag="div"
      class="d-flex flex-row justify-content-center mt-1 bg-light ranks h-100"
      @add="addToRankedImages"
    >
      <h1 v-if="showDragabbleHint" class="text-dark my-auto">
        Drag n' Drop Images Here
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
          triggers="hover focus"
          placement="top"
        >
          <b-img fluid :src="imgUrl" />
        </b-popover>
      </div>
    </Draggable>
  </b-container>
</template>

<script>
// import _ from 'lodash'

export default {
  name: 'ImagesPanel',
  props: {
    numRanks: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      rankedImages: [],
      images: this.random_images(16),
    }
  },
  computed: {
    ranksFull() {
      return this.rankedImages.length < this.numRanks
    },
    showDragabbleHint() {
      return this.rankedImages.length === 0
    },
  },
  methods: {
    random_images(n) {
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
      this.rankedImages = [...new Set(this.rankedImages)]
    },
  },
}
</script>

<style scoped>
.ranks {
  min-height: 130px;
  max-height: 130px;
}
</style>
