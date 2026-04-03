<template>
  <div class="token">
    <div class="pet-image">
      <img v-if="pictureUrl" :src="pictureUrl" alt="pet picture" />
      <img
        v-else-if="species === 'DOG'"
        class="placeholder"
        alt="pet icon placeholder"
        :src="dogIcon"
      />
    </div>
    <p class="pet-name">{{ name }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import dogIcon from '@/assets/icons/dog.png'

export default defineComponent({
  name: 'PetTokenComponent',
  components: {},
  props: {
    name: {
      type: String,
      required: true
    },
    pictureUrl: {
      type: String,
      required: false
    },
    species: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      dogIcon
    }
  }
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
  color: black;
}
</style>
