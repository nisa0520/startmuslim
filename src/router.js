import { createRouter, createWebHistory } from 'vue-router'
import { auth, loadUser } from './auth'
import Landing from './views/Landing.vue'
import Auth from './views/Auth.vue'
import PasswordReset from './views/PasswordReset.vue'
import Dashboard from './views/Dashboard.vue'
import StudentQuiz from './views/StudentQuiz.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Landing },
    { path: '/id', redirect: '/' },
    { path: '/masuk', component: Auth, props: { mode: 'login' }, meta: { guest: true } },
    { path: '/daftar', component: Auth, props: { mode: 'register' }, meta: { guest: true } },
    { path: '/lupa-kata-sandi', component: PasswordReset, props: { mode: 'request' } },
    { path: '/reset-password', component: PasswordReset, props: { mode: 'reset' } },
    { path: '/student/quiz', component: StudentQuiz, meta: { auth: true, student: true } },
    { path: '/dashboard', component: Dashboard, meta: { auth: true } },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to) => {
  if (!auth.ready) await loadUser()
  if (to.meta.auth && !auth.user) return '/masuk'
  if (to.meta.student && auth.user.role !== 'siswa') return '/dashboard'
  if (to.meta.guest && auth.user) return '/dashboard'
})

export default router
