<template>
  <div class="floating-button-container">
    <a :href="documentationLink" target="_blank" class="floating-button">
      <DocumentIcon class="icon" />
      <span class="tooltip">View Docs</span>
    </a>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { DocumentIcon } from '@heroicons/vue/24/solid'

export default defineComponent({
  name: 'FloatingButtonComponent',
  components: {
    DocumentIcon
  },
  data() {
    return {
      documentationLink: 'https://docs-pet-food-advice.firebaseapp.com'
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';
.floating-button-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.floating-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to right, $sidebar-background-color, $primary-color);
  border: none;
  border-radius: 50%;
  padding: 15px;
  color: $white-color-ref;
  text-decoration: none;
  transition:
    transform 0.3s,
    width 0.3s;
  overflow: hidden;
  white-space: nowrap;
  width: 60px;
  height: 60px;
}

.floating-button .icon {
  height: 24px;
  width: 24px;
  transition: transform 0.3s;
}

.floating-button:hover {
  width: 160px;
  border-radius: 30px;
}

.tooltip {
  display: inline-block;
  margin-left: 0;
  opacity: 0;
  transition: opacity 0.3s;
  visibility: hidden;
  width: 0;
  overflow: hidden;
}

.floating-button:hover .tooltip {
  opacity: 1;
  visibility: visible;
  width: auto;
  margin-left: 10px;
}
</style>
