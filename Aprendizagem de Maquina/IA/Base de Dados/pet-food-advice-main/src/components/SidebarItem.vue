<template>
  <router-link :to="link.route">
    <li :class="{ disabled: link.disabled }">
      <component :is="link.icon" class="mr-4 h-6 w-6" />
      {{ link.name }}
    </li>
  </router-link>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { Link } from '@/types/Utils'

export default defineComponent({
  name: 'SidebarItemComponent',
  props: {
    link: {
      type: Object as PropType<Link>,
      required: true
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';

li {
  cursor: pointer;
  font-weight: 400;
  font-size: 1rem;
  line-height: 1.5rem;
  font-family: 'Inter', sans-serif;
  padding: 8px;
  margin-top: 4px;
  color: $primary-color-fade;
  display: flex;
  flex-direction: row;
  align-items: center;
  transition: all 0.2s ease-in-out;
}

li:hover {
  color: $white-color-ref;
  background-color: $sidebar-background-color;
  border-radius: 4px;
  transition: all 0.2s ease-in-out;
}

.active {
  color: $white-color-ref;
  background-color: #362f78;
  border-radius: 4px;
}

.disabled {
  color: rgb(180 198 252 / 0.5);
  cursor: not-allowed;
}
</style>
