
// https://v3.nuxtjs.org/docs/directory-structure/nuxt.config
export default defineNuxtConfig({
    app: {
        // head
        head: {
            title: 'Element Plus + Nuxt 3',
            meta: [
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                {
                    hid: 'description',
                    name: 'description',
                    content: 'ElementPlus + Nuxt3',
                },
            ],
            link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
        }
    },
    routeRules: {
        // Homepage pre-rendered at build time
        '/': { prerender: true },
        // Product page generated on-demand, revalidates in background
        '/products/**': { swr: 3600 },
        // Blog post generated on-demand once until next deploy
        '/blog/**': { isr: true },
        // Admin dashboard renders only on client-side
        '/admin/**': { ssr: false },
        // Add cors headers on API routes
        '/*': { cors: true },
        // Redirects legacy urls
        '/old-page': { redirect: '/new-page' }
    },
    // css
    css: ['~/assets/scss/index.scss'],

    typescript: {
        strict: true,
        shim: false,
    },

    // build modules
    modules: [
        '@vueuse/nuxt',
        '@unocss/nuxt',
        '@pinia/nuxt',
        '@element-plus/nuxt',
        '@nuxtjs/color-mode'
    ],

    // vueuse
    vueuse: {
        ssrHandlers: true,
    },

    // colorMode
    colorMode: {
        classSuffix: '',
    },

    unocss: {
        uno: true,
        attributify: true,
        icons: {
            scale: 1.2,
        },
    },
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: `@use "@/assets/scss/element/index.scss" as element;`,
                },
            },
        },
    },
    elementPlus: {
        icon: 'ElIcon',
        importStyle: 'scss',
        themes: ['dark'],
    },
})
