import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: 'Pet Food Advice',
  themeConfig: {
    nav: [
      { text: 'Project Scope', link: '/project-scope' },
      { text: 'Ideation Process', link: '/ideation-process' },
      { text: 'Feature Enhancements', link: '/feature-enhancements' },
      { text: 'About me', link: '/about' }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/clarabatt/pet-food-advice' },
      { icon: 'linkedin', link: 'https://www.linkedin.com/in/clara-battesini/' }
    ]
  }
})
