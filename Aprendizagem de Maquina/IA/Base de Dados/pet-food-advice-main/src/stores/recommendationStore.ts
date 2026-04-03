import { toRaw } from 'vue'
import { defineStore } from 'pinia'
import {
  getDogFoodRecommendations,
  type RecommendationResponse
} from '@/services/recommendationApi'
import type { Pet } from '@/types/Pet'

export const useRecommendationStore = defineStore('recommendationStore', {
  state: () => ({
    selectedPet: null as Pet | null,
    petConditions: [] as string[],
    recommendations: [] as RecommendationResponse[],
    isLoading: false
  }),

  actions: {
    selectPet(pet: Pet) {
      this.selectedPet = pet
    },
    addCondition(condition: string) {
      if (!this.petConditions.includes(condition)) {
        const newConditions = [...this.petConditions, condition]
        this.petConditions = newConditions
      }
    },
    removeCondition(condition: string) {
      const index = this.petConditions.indexOf(condition)
      if (index > -1) {
        this.petConditions.splice(index, 1)
      }
    },
    toggleCondition(condition: string) {
      if (this.petConditions.includes(condition)) {
        this.removeCondition(condition)
      } else {
        this.addCondition(condition)
      }
    },
    fetchRecommendations() {
      if (!this.selectedPet) {
        throw new Error('No pet selected')
      }

      let weight: number = Number(this.selectedPet.weight.value)

      if (this.selectedPet.weight.is_metric == 1) {
        weight = weight * 2.205
      }

      const payload = {
        breed: this.selectedPet.breed,
        age: this.selectedPet.age,
        animalWeight: weight,
        conditions: toRaw(this.petConditions)
      }

      this.isLoading = true

      getDogFoodRecommendations(payload)
        .then((result) => {
          this.recommendations = result
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  },

  getters: {
    hasSelectedPet: (state) => state.selectedPet !== null,
    getRecommendations: (state) => state.recommendations
  }
})
