<template>
  <b-form>
    <b-form-row>
      <ImagesPanel />
    </b-form-row>
    <b-form-row>
      <b-button-group class="w-100 mt-3">
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-button-group>
    </b-form-row>
  </b-form>
</template>

<script>
import ImagesPanel from '~/components/ImagesPanel'

export default {
  name: 'RankingForm',
  components: { ImagesPanel },
}
</script>

<style scoped></style>
