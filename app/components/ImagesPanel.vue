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
            thumbnail
            fluid
            :src="imgUrl"
            height="130px"
            width="130px"
          ></b-img>
        </b-col>
      </Draggable>
    </b-container>

    <Draggable
      :list="rankedImages"
      :group="{ name: 'images', put: ranksFull }"
      class="row text-left mt-1 bg-light ranks"
      @add="addToRankedImages"
    >
      <b-col v-for="(imgUrl, idx) in rankedImages" :key="idx">
        <b-avatar
          rounded="sm"
          :src="imgUrl"
          :badge="`${idx + 1}`"
          size="130px"
          badge-top
        ></b-avatar>
      </b-col>
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
  },
  methods: {
    random_images(n) {
      const res = []
      let i
      for (i = 0; i < n; i++) {
        res.push(`https://picsum.photos/id/${i + 20}/125/125`)
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
  height: 130px;
  max-height: 130px;
}
</style>
