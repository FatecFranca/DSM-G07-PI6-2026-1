<template>
  <nav :class="['sidebar', { 'show-sidebar': isSidebarOpen }]">
    <div class="sidebar-logo">
      <!-- <img src="/logo.png" alt="logo" /> -->
      <ArrowLeftIcon class="h-6 w-6 menu-icon text-[#b4c6fc]" @click="toggleSidebar" />
    </div>
    <ol class="sidebar-links">
      <SidebarItem v-for="link in links" :key="link.name" :link="link" />
    </ol>
  </nav>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import {
  Square3Stack3DIcon,
  PencilSquareIcon,
  BellIcon,
  Cog6ToothIcon,
  LifebuoyIcon,
  UserIcon,
  SparklesIcon,
  ClipboardDocumentListIcon
} from '@heroicons/vue/24/outline'
import SidebarItem from './SidebarItem.vue'
import { ArrowLeftIcon } from '@heroicons/vue/24/solid'
import type { Link } from '@/types/Utils'

export default defineComponent({
  name: 'SidebarComponent',
  components: { SidebarItem, ArrowLeftIcon },
  setup() {
    const isSidebarOpen = ref<boolean>(false)
    const links = ref<Link[]>([
      { name: 'Dashboard', icon: Square3Stack3DIcon, route: '/', disabled: false },
      { name: 'Appointments', icon: UserIcon, route: '/', disabled: true },
      { name: 'Book vet appointment', icon: ClipboardDocumentListIcon, route: '/', disabled: true },
      { name: 'Food Advice', icon: SparklesIcon, route: '/food-advice', disabled: false },
      { name: 'Prescriptions', icon: PencilSquareIcon, route: '/', disabled: true },
      { name: 'Notifications', icon: BellIcon, route: '/', disabled: true },
      { name: 'Help', icon: LifebuoyIcon, route: '/', disabled: true },
      { name: 'Account', icon: Cog6ToothIcon, route: '/', disabled: true }
    ])

    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value
    }

    return { links, toggleSidebar, isSidebarOpen }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/variables.scss';

.sidebar {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  width: $sidebar-width;
  min-height: 100vh;
  background-color: $primary-color;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  transform: translateX(0);
  transition: transform 0.5s ease-out;
}

.sidebar > .sidebar-logo {
  padding: 1.7rem;
  display: flex;
  justify-content: flex-end;
}

.sidebar > .sidebar-links {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 1rem 0.5rem;
  color: $white-color-ref;
}

@media only screen and (max-width: $layout-breakpoint-small) {
  .sidebar {
    transform: translateX(-100%);
    width: 250px;
    overflow: auto;
  }

  .show-sidebar {
    transform: translateX(0);
  }
}
</style>
