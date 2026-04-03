<template>
    <nav class="site-nav">
      <RouterLink to="/" class="nav-link">Robot Controls</RouterLink>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
      <RouterLink to="/likes" class="nav-link">Likes</RouterLink>
    </nav>
</template>

<style scoped>
.site-nav {
display: flex;
gap: 0.75rem;
}

.nav-link {
color: white;
text-decoration: none;
padding: 0.5rem 0.75rem;
border-radius: 6px;
}

.nav-link:hover {
background: rgba(255, 255, 255, 0.12);
}
</style>