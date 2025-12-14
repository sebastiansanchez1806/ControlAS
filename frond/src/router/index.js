import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useAdminStore } from '@/stores/admin';
import { useGestorPrincipalStore } from '@/stores/gestorPrincipal'; // ← NUEVO IMPORT
import info_locales from '@/components/admin panel/info_locales.vue';
import LoginView from '@/components/login.vue';
import LocalesView from '@/components/locales.vue';
import Personal_femenino from '@/components/personal_femenino.vue';
import Jefe_productos from '@/components/jefe_productos.vue';
import Administradores from '@/components/administradores.vue';
import Historial from '@/components/historial.vue';
import Administrador_parte from '@/components/administrador_parte.vue';
import Factura_admin from '@/components/factura_admin.vue';
import Facturas from '@/components/facturas.vue';
import Datos_jefe from '@/components/datos_jefe.vue';
import Recuperar_contra from '@/components/recuperar_contra.vue';
import Agregar_admin from '@/components/agregar_admin.vue';
import Login_principal from '@/components/admin panel/login_principal.vue';
import Home_admin_principal from '@/components/admin panel/home_admin_principal.vue';
import Tareas_admin from '@/components/Tareas_admin.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  {
    path: '/login_gestor_principal_diego',
    name: 'LoginGestorPrincipal',
    component: Login_principal
  },
  {
  path: '/info_locales/:barId',
  name: 'InfoLocales',
  component: info_locales,
  props: true,  // Para que reciba barId como prop
  meta: { requiresGestorPrincipal: true }  // Solo accesible si estás logueado como gestor principal
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
  const gestorStore = useGestorPrincipalStore();

  const isDueno = userStore.isLoggedIn && userStore.tipo === 'dueno';
  const isAdmin = adminStore.id !== null;
  const isGestorPrincipal = gestorStore.isLoggedIn();

  // === PROTECCIÓN PARA GESTOR PRINCIPAL (todas las rutas con meta.requiresGestorPrincipal) ===
  if (to.meta.requiresGestorPrincipal) {
    return isGestorPrincipal 
      ? next() 
      : next({ name: 'LoginGestorPrincipal' });
  }

  // Si está logueado como gestor y va al login, redirigir al panel
  if (to.name === 'LoginGestorPrincipal' && isGestorPrincipal) {
    return next({ name: 'home_admin_principal' });
  }

  // === RUTAS NORMALES DE DUEÑO Y ADMIN ===
  const isAuthenticated = isDueno || isAdmin;
  const isPublicRoute = to.name === 'Login' || to.name === 'recuperar';

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'Login' });
  }

  if (isPublicRoute && isAuthenticated) {
    return isDueno ? next({ name: 'Locales' }) : next({ name: 'administrador_parte' });
  }

  if (to.meta.requiresAuth) {
    if (to.meta.requiresDueno && !isDueno) return next({ name: 'administrador_parte' });
    if (to.meta.requiresAdmin && !isAdmin) return next({ name: 'Locales' });
  }

  next();
});
export default router;