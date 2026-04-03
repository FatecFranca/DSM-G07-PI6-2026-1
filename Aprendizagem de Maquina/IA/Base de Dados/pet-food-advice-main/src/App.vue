<template>
  <Sidebar ref="sidebarRef" />
  <div class="main-panel">
    <Menubar :button-action="toggleSidebar" />
    <main>
      <RouterView />
    </main>
  </div>
  <DocumentationButton />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Menubar from './components/Menubar.vue'
import { useUserStore } from '@/stores/userStore'
import DocumentationButton from '@/components/DocumentationButton.vue'

export default defineComponent({
  name: 'App',
  components: { Sidebar, Menubar, RouterView, DocumentationButton },
  setup() {
    const sidebarRef = ref<InstanceType<typeof Sidebar> | null>(null)

    const toggleSidebar = () => {
      if (sidebarRef.value) {
        sidebarRef.value.toggleSidebar()
      }
    }

    const userStore = useUserStore()
    onMounted(() => {
      userStore.fetchUser()
    })
    return { toggleSidebar, sidebarRef }
  }
})
</script>

<style lang="scss">
@import '@/assets/variables.scss';

.main-panel {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding-left: $sidebar-width;
}

main {
  position: relative;
  width: 80%;
  min-height: 90%;
  box-sizing: border-box;
  margin: 0 2rem 2rem 2rem;
  padding: 2rem;
  margin-top: calc($menubar-height + 2rem);
  background-color: $white-color-ref;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

@media only screen and (max-width: $layout-breakpoint-small) {
  main {
    width: 95%;
    padding: 1rem;
    margin-top: calc($menubar-height + 1rem);
  }
  .main-panel {
    padding-left: 0;
  }
}
</style>
