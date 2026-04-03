<template>
  <div class="petFood">
    <div class="image">
      <img :src="food.picture" alt="food.name" />
    </div>
    <div class="stats">
      <div class="description">
        <h3 class="brand">{{ food.brand }}</h3>
        <h2 class="name">{{ food.name }}</h2>
        <p>Suggested daily dose:</p>
        <h3 class="dailyAmount">280g</h3>
        <h5 class="details">
          *Amount may vary based on animal's condition. Please consult Vetster's veterinarian.
        </h5>
      </div>
      <div class="subscription">
        <Price :price="food.price" />
        <p class="description">
          Delivered monthly at your place<br />
          + Healthy organic treat pack
        </p>
        <ButtonComponent> Sign up for {{ food.brand }} </ButtonComponent>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { type RecommendationResponse } from '@/services/recommendationApi'
import ButtonComponent from '@/components/Button.vue'
import Price from '@/components/Price.vue'

export default defineComponent({
  name: 'PetFoodSubscriptionComponent',
  props: {
    food: {
      type: Object as PropType<RecommendationResponse>,
      required: true
    }
  },
  components: { ButtonComponent, Price }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';

.petFood {
  width: 90%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
  padding: 2.5rem 0;
  border-bottom: 1px solid #e5e5e5;
}

.petFood:last-child {
  border-bottom: none;
}

.petFood > .image {
  width: 30%;
  display: flex;
  justify-content: flex-end;
  img {
    width: 100%;
    max-width: 20rem;
  }
}

.stats {
  width: 70%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 1rem 0;
}

.stats > .description {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 1rem;
  width: 70%;
}

.stats > .description > .brand {
  font-size: 1rem;
  font-weight: 600;
  margin: 0.35rem 0 0 0;
}

.stats > .description > .name {
  font-size: 1.15rem;
  margin: 0.3rem 0 0.5rem 0;
}

.stats > .description > p {
  font-size: 0.75rem;
  margin-top: 0.75rem;
}

.stats > .description > .dailyAmount {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0.3rem 0 0 0;
}

.stats > .description > .details {
  font-size: 0.75rem;
  margin-top: 0.8rem;
}

.stats > .subscription {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 1rem;
}

.stats > .subscription > .description {
  font-size: 0.75rem;
  padding: 0 1.5rem 1rem 1.5rem;
}

@media only screen and (max-width: $layout-breakpoint-medium) {
  .stats {
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .stats > .subscription {
    width: 100%;
    align-items: flex-start;
    text-align: left;
  }

  .stats > .subscription > .description {
    padding: 0 0 1rem 0;
  }
}

@media only screen and (max-width: $layout-breakpoint-small) {
  .petFood {
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .stats {
    width: 100%;
  }

  .stats > .description {
    align-items: center;
    text-align: center;
  }

  .stats > .description > .brand {
    font-size: 1.1rem;
  }

  .stats > .description > .name {
    font-size: 1.5rem;
  }

  .stats > .description > p {
    font-size: 0.9rem;
  }

  .stats > .description > .dailyAmount {
    font-size: 1.75rem;
  }

  .stats > .description > .details {
    font-size: 0.9rem;
  }

  .stats > .subscription {
    align-items: center;
    text-align: center;
  }

  .stats > .subscription > .description {
    font-size: 0.9rem;
    padding-bottom: 1.5rem;
  }
}
</style>
