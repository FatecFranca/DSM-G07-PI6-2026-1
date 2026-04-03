<template>
  <div class="load" v-if="isPetLoading || isRecommendationLoading">
    <Loading />
  </div>
  <div v-else>
    <Step1 v-if="state.currentStep === 1" :pets="availablePets" :setPet="setPet" />
    <Step2 v-if="state.currentStep === 2" :goToNextStep="getRecommendation" />
    <Step3 v-if="state.currentStep === 3" :petName="selectedPet?.name" />

    <button class="back-icon" v-if="state.currentStep > 1" @click="goToPreviousStep">
      <ArrowLeftIcon style="height: 1.2rem; margin: 0.25rem" />
      Back
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, reactive } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRecommendationStore } from '@/stores/recommendationStore'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import Loading from '@/components/Loading.vue'
import type { Pet } from '@/types/Pet'

import Step1 from './Step1.vue'
import Step2 from './Step2.vue'
import Step3 from './Step3.vue'

export default defineComponent({
  name: 'FoodAdviceView',
  setup() {
    const recommendationStore = useRecommendationStore()
    const userStore = useUserStore()

    const totalSteps = ref<Number>(3)
    const state = reactive({
      currentStep: 1
    })

    const availablePets = computed(() => userStore.getPetsList)
    const isPetLoading = computed(() => userStore.getIsLoading)
    const isRecommendationLoading = computed(() => recommendationStore.isLoading)
    const foodRecommendations = computed(() => recommendationStore.getRecommendations)
    const selectedPet = computed(() => recommendationStore.selectedPet)

    const getRecommendation = () => {
      recommendationStore.fetchRecommendations()
      goToNextStep()
    }

    const setPet = (pet: Pet) => {
      recommendationStore.selectPet(pet)
      goToNextStep()
    }

    const goToNextStep = () => {
      if (state.currentStep < Number(totalSteps.value)) {
        state.currentStep++
      }
    }

    const goToPreviousStep = () => {
      if (state.currentStep > 1) {
        state.currentStep--
      }
    }

    return {
      availablePets,
      selectedPet,
      state,
      isPetLoading,
      isRecommendationLoading,
      goToNextStep,
      goToPreviousStep,
      totalSteps,
      setPet,
      foodRecommendations,
      getRecommendation
    }
  },
  components: {
    Step1,
    Step2,
    Step3,
    ArrowLeftIcon,
    Loading
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';
.load {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.back-icon {
  display: flex;
  justify-content: left;
  align-items: center;
  margin: 2rem 0 0 1rem;
  width: 100%;
}

@media only screen and (max-width: $layout-breakpoint-small) {
  .back-icon {
    margin-left: 0;
  }
}
</style>
