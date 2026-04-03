<template>
  <div class="priceComponent">
    <p>$</p>
    <p class="price">{{ price.toFixed(0) }}</p>
    <p>/month</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PetFoodSubscriptionComponent',
  props: {
    price: {
      type: Number,
      required: true
    }
  },
  components: {}
})
</script>

<style lang="scss" scoped>
.priceComponent {
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  justify-content: center;
  margin: 1.5rem 0;
}

.priceComponent > .price {
  font-size: 2.3rem;
  font-weight: 600;
  margin: 0 0.5rem;
  line-height: 0.8;
}
</style>
