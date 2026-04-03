<template>
  <h1>Who is the food for?</h1>
  <div class="pets">
    <PetToken
      @click="setPet(pet)"
      v-for="pet in pets"
      :key="pet.id"
      :name="pet.name"
      :species="pet.species"
    />
    <AddPet @click="handleAddPet" />
  </div>
  <ToastWarning ref="toastRef" message="It's not possible to add a pet now" />
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue'
import type { Pet } from '@/types/Pet'
import PetToken from '@/components/PetToken.vue'
import AddPet from '@/components/AddPet.vue'
import ToastWarning from '@/components/ToastWarning.vue'

export default defineComponent({
  name: 'Step1View',
  props: {
    pets: {
      type: Array as PropType<Pet[]>,
      required: true
    },
    setPet: {
      type: Function as PropType<(pet: Pet) => void>,
      required: true
    }
  },
  setup() {
    const toastRef = ref<InstanceType<typeof ToastWarning> | null>(null)

    const handleAddPet = () => {
      if (toastRef.value) {
        toastRef.value.showToast()
      }
    }

    return { handleAddPet, toastRef }
  },
  components: {
    PetToken,
    AddPet,
    ToastWarning
  }
})
</script>

<style lang="scss" scoped>
h1 {
  text-align: center;
  margin-top: 6rem;
}
.pets {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
}
</style>
