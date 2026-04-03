<template>
  <div class="component-container">
    <h1>Pet Food Advice</h1>

    <p>
      Pet Food Advice is a web application that helps pet owners to find the best food for their
      pets.
    </p>

    <div class="badges">
      <a href="https://github.com/clarabatt/pet-food-advice" target="_blank">
        <img
          src="https://img.shields.io/badge/-Project%20Repo-333?style=flat&logo=github"
          alt="GitHub Project Repo"
        />
      </a>
      <a href="https://www.linkedin.com/in/clara-battesini/" target="_blank">
        <img
          src="https://img.shields.io/badge/-LinkedIn%20Profile-0077B5?style=flat&logo=linkedin"
          alt="LinkedIn Profile"
        />
      </a>
      <a href="mailto:clarabattesini@gmail.com">
        <img
          src="https://img.shields.io/badge/-Email-D14836?style=flat&logo=gmail&logoColor=white"
          alt="Email"
        />
      </a>
      <a href="https://docs-pet-food-advice.firebaseapp.com/" target="_blank">
        <img
          src="https://img.shields.io/badge/-Documentation-0175C2?style=flat"
          alt="Documentation"
        />
      </a>
    </div>
    <ButtonComponent @click="goToFoodAdvice">Go to Food Advice</ButtonComponent>
    <p class="developer-credit">
      Developed by: <a href="https://github.com/clarabatt" target="_blank"> Clara Battesini</a>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ButtonComponent from '@/components/Button.vue'

export default defineComponent({
  name: 'HomeView',
  methods: {
    goToFoodAdvice() {
      this.$router.push('/food-advice')
    }
  },
  components: {
    ButtonComponent
  }
})
</script>

<style scoped>
.component-container {
  text-align: center;
  padding: 20px;
}

.badges {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.badges > a {
  margin: 0 0.5rem;
}

.developer-credit {
  margin-top: 2rem;
  font-size: 1rem;
  font-weight: 300;
}
</style>
