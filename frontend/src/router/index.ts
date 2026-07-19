import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/public/HomePage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/public/LoginPage.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/public/RegisterPage.vue'),
      meta: { guest: true },
    },
    {
      path: '/customize',
      name: 'customize',
      component: () => import('@/views/public/CustomizePage.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/user/ProfilePage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/orders/:id',
      name: 'orderDetail',
      component: () => import('@/views/user/OrderDetailPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'adminDashboard',
          component: () => import('@/views/admin/AdminDashboard.vue'),
        },
        {
          path: 'users',
          name: 'adminUsers',
          component: () => import('@/views/admin/AdminUsers.vue'),
        },
        {
          path: 'orders',
          name: 'adminOrders',
          component: () => import('@/views/admin/AdminOrders.vue'),
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notFound',
      component: () => import('@/views/public/NotFoundPage.vue'),
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    if (!authStore.isLoggedIn) {
      next({ name: 'login', query: { redirect: to.fullPath } })
    } else {
      next({ name: 'home' })
    }
    return
  }

  if (to.meta.guest && authStore.isLoggedIn) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router
