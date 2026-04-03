<template>
  <div :class="['token', { isTokenActive: isActive }]" @click="handleClick">
    <div class="condition-icon">
      <img v-if="iconUrl" :src="iconUrl" alt="icon" />
      <img
        v-else-if="name === 'Allergies or Food Sensitivities'"
        class="icon"
        alt="whealthy with a block icon on it"
        :src="condition_diet_icon"
      />
      <img
        v-else-if="name === 'Digestive issues'"
        class="icon"
        alt="intestine with a check icon on it"
        :src="condition_digestive_icon"
      />
      <img
        v-else-if="name === 'Dental issues'"
        class="icon"
        alt="tooth with a plus icon on it"
        :src="condition_dental_icon"
      />
      <img
        v-else-if="name === 'Mobility concerns'"
        class="icon"
        alt="Two bones close to each other"
        :src="condition_joint_icon"
      />
      <img
        v-else-if="name === 'Skin/Coat problems'"
        class="icon"
        alt="skin with a hair growing icon"
        :src="condition_skin_icon"
      />
      <img
        v-else-if="name === 'Urinary problems'"
        class="icon"
        alt="kidneys"
        :src="condition_kidney_icon"
      />
      <img
        v-else-if="name === 'Overweight'"
        class="icon"
        alt="scale indicating overweight"
        :src="condition_overweight_icon"
      />
    </div>
    <p class="condition-name">{{ name }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { PetCondition } from '@/types/Pet'
import type { Icon } from '@/types/Utils'
import condition_dental_icon from '@/assets/icons/condition_dental.png'
import condition_diet_icon from '@/assets/icons/condition_diet.png'
import condition_digestive_icon from '@/assets/icons/condition_digestive.png'
import condition_joint_icon from '@/assets/icons/condition_joint.png'
import condition_kidney_icon from '@/assets/icons/condition_kidney.png'
import condition_skin_icon from '@/assets/icons/condition_skin.png'
import condition_overweight_icon from '@/assets/icons/condition_overweight.png'

export default defineComponent({
  name: 'ConditionTokenComponent',
  components: {},
  props: {
    name: {
      type: String as PropType<PetCondition>,
      required: true
    },
    iconUrl: {
      type: String,
      required: false
    },
    icon: {
      type: Object as PropType<Icon>,
      required: false
    },
    isActive: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  methods: {
    handleClick() {
      this.$emit('childEvent', this.name)
    }
  },
  data() {
    return {
      condition_dental_icon,
      condition_diet_icon,
      condition_digestive_icon,
      condition_joint_icon,
      condition_kidney_icon,
      condition_skin_icon,
      condition_overweight_icon
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
  margin: 1rem 0.5rem;
  height: 6rem;
  width: 11rem;
  cursor: pointer;
  border: rgb(205 219 254) solid 1px;
  border-radius: 0.5rem;
  transition: all 0.15s ease-in-out;
}

.token:hover {
  outline: solid 2px rgb(104 117 245);
  transition: all 0.15s ease-in-out;
}
.isTokenActive {
  outline: solid 2px rgb(104 117 245);
  transition: all 0.15s ease-in-out;
}

.condition-image > img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.condition-image > .placeholder {
  width: 3.5rem !important;
  object-fit: contain;
}

.condition-name {
  text-align: center;
  margin-top: 0.5rem;
  font-weight: 300;
  color: black;
}
</style>
@/sfc
