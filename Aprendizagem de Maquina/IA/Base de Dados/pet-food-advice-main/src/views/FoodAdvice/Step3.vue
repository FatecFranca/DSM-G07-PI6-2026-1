<template>
  <div class="foodRecommendations">
    <div class="title">
      <SparklesIcon class="w-10 h-10 text-yellow-500" />
      <h1>Recommended options for {{ petName ? petName : 'your pet' }}:</h1>
    </div>
    <PetFoodSubscription v-for="food in foodList" :key="food._id" :food="food" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import { useRecommendationStore } from '@/stores/recommendationStore'
import type { RecommendationResponse } from '@/services/recommendationApi'
import PetFoodSubscription from '@/components/PetFoodSubscription.vue'
import { SparklesIcon } from '@heroicons/vue/24/solid'

export default defineComponent({
  name: 'Step3View',
  props: {
    petName: {
      type: String,
      required: false
    }
  },
  components: { PetFoodSubscription, SparklesIcon },
  setup() {
    const recommendationStore = useRecommendationStore()

    const foodList = computed<RecommendationResponse[]>(
      () => recommendationStore.getRecommendations
    )

    return {
      recommendationStore,
      foodList
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';
.foodRecommendations {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 2rem 0;
}

.foodRecommendations > .title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
}

.foodRecommendations > .title > h1 {
  margin: 0 0 0 0.5rem;
}

@media only screen and (max-width: $layout-breakpoint-medium) {
  .foodRecommendations > .title > h1 {
    font-size: 1.8rem;
  }
}
</style>
