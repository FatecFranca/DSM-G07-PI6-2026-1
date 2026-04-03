<template>
  <button
    type="button"
    class="btn bg-gradient-to-r from-[#ec4899] to-[#be185d] hover:from-[#be185d] hover:to-[#831843]"
    @click="handleClick"
  >
    <slot></slot>
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ButtonComponent',
  emits: ['click'],
  methods: {
    handleClick() {
      this.$emit('click')
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';
.btn {
  font-size: 1.125rem;
  line-height: 1.75rem;
  padding: 1rem 1.5rem;
  border-style: solid;
  border-color: #e5e7eb;
  color: $white-color-ref;

  transition: all 0.15s ease-in-out;
  border-radius: 0.375rem;
  width: 18rem;
  font-weight: 400;
}

.btn:hover {
  transition: all 0.15s ease-in-out;
}
</style>
