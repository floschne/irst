<template>
  <b-form>
    <b-form-row>
      <RankingPanel :num_ranks="10" />
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
import RankingPanel from '~/components/RankingPanel'

export default {
  name: 'RankingForm',
  components: { RankingPanel },
}
</script>

<style scoped></style>
