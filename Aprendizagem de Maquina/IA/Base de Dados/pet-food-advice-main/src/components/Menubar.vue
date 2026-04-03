<template>
  <div class="menubar">
    <Bars3Icon @click="handleClick" class="h-6 w-6 menu-icon" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Bars3Icon } from '@heroicons/vue/24/outline'

export default defineComponent({
  name: 'MenubarComponent',
  components: { Bars3Icon },
  props: {
    buttonAction: {
      type: Function,
      required: true
    }
  },
  setup(props) {
    const handleClick = () => {
      if (props.buttonAction) {
        props.buttonAction()
      }
    }

    return { handleClick }
  }
})
</script>

<style lang="scss">
@import '@/assets/variables.scss';

.menubar {
  display: flex;
  position: fixed;
  z-index: 1000;
  width: calc(100% - $sidebar-width);
  height: $menubar-height;
  background-color: $white-color-ref;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  padding: 1rem 2rem;
  z-index: 1111;
}

.menu-icon {
  display: none;
}

@media only screen and (max-width: $layout-breakpoint-small) {
  .menubar {
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .menu-icon {
    display: flex;
    cursor: pointer;
  }
}
</style>
