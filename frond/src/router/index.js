import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useAdminStore } from '@/stores/admin';
import { useGestorPrincipalStore } from '@/stores/gestorPrincipal'; // ← NUEVO IMPORT

import LoginView from '@/components/login.vue';
import LocalesView from '@/components/locales.vue';
import Personal_femenino from '@/components/personal_femenino.vue';
import Jefe_productos from '@/components/jefe_productos.vue';
import Administradores from '@/components/administradores.vue';
import Historial from '@/components/historial.vue';
import Administrador_parte from '@/components/administrador_parte.vue';
import Tareas_admin from '@/components/tareas_admin.vue';
import Factura_admin from '@/components/factura_admin.vue';
import Facturas from '@/components/facturas.vue';
import Datos_jefe from '@/components/datos_jefe.vue';
import Recuperar_contra from '@/components/recuperar_contra.vue';
import Agregar_admin from '@/components/agregar_admin.vue';
import Login_principal from '@/components/admin panel/login_principal.vue';
import Home_admin_principal from '@/components/admin panel/home_admin_principal.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  {
    path: '/login_gestor_principal_diego',
    name: 'LoginGestorPrincipal',
    component: Login_principal
  },
  {
    path: '/home_admin_principal',
    name: 'home_admin_principal',
    component: Home_admin_principal,
    meta: { requiresGestorPrincipal: true }
  },
  { path: '/agregar_admin', name: 'agregar_admin', component: Agregar_admin },
  { path: '/femenino', name: 'femenino', component: Personal_femenino, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/jefe_productos', name: 'jefe_productos', component: Jefe_productos, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/configuracion', name: 'configuracion', component: Datos_jefe, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/recuperar', name: 'recuperar', component: Recuperar_contra },
  { path: '/administradores', name: 'administradores', component: Administradores, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/historial', name: 'historial', component: Historial, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/administrador_parte', name: 'administrador_parte', component: Administrador_parte, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/factura_admin', name: 'factura_admin', component: Factura_admin, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/tareas', name: 'tareas', component: Tareas_admin, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/locales', name: 'Locales', component: LocalesView, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/facturas', name: 'facturas', component: Facturas, meta: { requiresAuth: true, requiresDueno: true } },
  { path: '/', redirect: '/login' },
  { path: '/:pathMatch(.*)*', name: 'NotFound', redirect: { name: 'Login' } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// GUARD GLOBAL ÚNICO Y BIEN ORDENADO
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const adminStore = useAdminStore();
  const gestorStore = useGestorPrincipalStore(); // ← EL STORE DEL GESTOR

  const isDueno = userStore.isLoggedIn && userStore.tipo === 'dueno';
  const isAdmin = adminStore.id !== null;
  const isGestorPrincipal = gestorStore.isLoggedIn();

  // 1. PROTECCIÓN DEL GESTOR PRINCIPAL (lo más importante primero)
  if (to.name === 'home_admin_principal') {
    return isGestorPrincipal ? next() : next({ name: 'LoginGestorPrincipal' });
  }

  if (to.name === 'LoginGestorPrincipal' && isGestorPrincipal) {
    return next({ name: 'home_admin_principal' });
  }

  // 2. RUTAS NORMALES DE DUEÑO Y ADMIN (tu lógica original)
  const isAuthenticated = isDueno || isAdmin;
  const isPublicRoute = to.name === 'Login' || to.name === 'recuperar';

  if (to.meta.requiresAuth && !isAuthenticated && !isGestorPrincipal) {
    return next({ name: 'Login' });
  }

  if (isPublicRoute && isAuthenticated) {
    return isDueno ? next({ name: 'Locales' }) : next({ name: 'administrador_parte' });
  }

  if (to.meta.requiresAuth) {
    if (to.meta.requiresDueno && !isDueno) return next({ name: 'administrador_parte' });
    if (to.meta.requiresAdmin && !isAdmin) return next({ name: 'Locales' });
  }

  // Todo bien
  next();
});

export default router;