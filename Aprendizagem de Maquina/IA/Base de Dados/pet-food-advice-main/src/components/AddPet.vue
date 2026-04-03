<template>
  <div class="token">
    <div class="pet-image">
      <PlusIcon style="color: #42389d; height: 2.3rem" />
    </div>
    <p class="pet-name">Add pet</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'

export default defineComponent({
  name: 'AddPetComponent',
  components: { PlusIcon }
})
</script>

<style lang="scss" scoped>
.token {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 1rem 3rem;
  cursor: pointer;
}

.pet-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 6rem;
  height: 6rem;
  border-radius: 100%;
  overflow: hidden;
  background-color: rgb(243 247 255);
  transition: all 0.1s ease-in-out;
}

.pet-image:hover {
  border-radius: 99999;
  outline: solid 4px rgb(88 80 236);
  transition: all 0.1s ease-in-out;
}

.pet-image > img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pet-image > .placeholder {
  width: 3.5rem !important;
  object-fit: contain;
}

.pet-name {
  text-align: center;
  margin-top: 0.5rem;
  font-weight: 400;
  color: rgb(66 56 157);
}
</style>
