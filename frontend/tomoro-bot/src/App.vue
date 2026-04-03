<script setup>
import SiteNav from './components/SiteNav.vue'
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="site-header-inner">
        <h1 class="site-title">TomoroBot Control Panel</h1>

        <SiteNav />
      </div>
    </header>

    <main class="page-content">
      <RouterView />
    </main>
  </div>
</template>