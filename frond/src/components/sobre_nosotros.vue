<template>
  <div class="controlas-container">
    <!-- Panel lateral de contacto (Desktop) -->
    <div class="contact-sidebar" :class="{ 'open': showContactPanel }">
      <div class="sidebar-content">
        <h3>📞 Contáctanos</h3>
        <p class="sidebar-subtitle">Estamos aquí para ayudarte</p>
        
        <a href="https://wa.me/573213686373" target="_blank" class="contact-option whatsapp">
          <div class="contact-icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
            </svg>
          </div>
          <div class="contact-info">
            <strong>WhatsApp</strong>
            <span>+57 321 368 6373</span>
          </div>
        </a>

        <a href="mailto:controlas302025@gmail.com" class="contact-option email">
          <div class="contact-icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="4" width="20" height="16" rx="2"></rect>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
            </svg>
          </div>
          <div class="contact-info">
            <strong>Email</strong>
            <span>controlas302025@gmail.com</span>
          </div>
        </a>

        <p class="sidebar-footer">¡Estamos listos para ayudarte!</p>
      </div>
    </div>

    <!-- Tab de contacto (Desktop) -->
    <div class="contact-tab" @click="toggleContactPanel">
      <svg v-if="!showContactPanel" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
      <span>Contáctanos</span>
    </div>

    <!-- Botón flotante (Mobile) -->
    <div class="floating-contact-mobile" @click="toggleContactModal">
      <svg v-if="!showContactModal" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </div>

    <!-- Modal de contacto (Mobile) -->
    <transition name="modal-fade">
      <div v-if="showContactModal" class="contact-modal-overlay" @click="toggleContactModal">
        <div class="contact-modal" @click.stop>
          <h3>📞 Contáctanos</h3>
          <p class="modal-subtitle">Estamos aquí para ayudarte</p>
          
          <a href="https://wa.me/573213686373" target="_blank" class="contact-option whatsapp">
            <div class="contact-icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
            </div>
            <div class="contact-info">
              <strong>WhatsApp</strong>
              <span>+57 321 368 6373</span>
            </div>
          </a>

          <a href="mailto:controlas302025@gmail.com" class="contact-option email">
            <div class="contact-icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
              </svg>
            </div>
            <div class="contact-info">
              <strong>Email</strong>
              <span>controlas302025@gmail.com</span>
            </div>
          </a>
        </div>
      </div>
    </transition>

    <!-- Sección: Quiénes Somos -->
    <section class="section who-we-are" :class="{ 'animate-in': section1Visible }" ref="section1">
      <div class="content-wrapper">
        <h1 class="section-title">
          <span class="title-line"></span>
          Quiénes Somos
          <span class="title-line"></span>
        </h1>
        
        <div class="intro-text">
          <p>
            Conocemos de cerca los desafíos de dirigir bares y establecimientos de entretenimiento adulto: 
            el control riguroso del inventario, el cierre de cuentas diario sin margen de error, la vigilancia 
            de los gastos pequeños que impactan el resultado final y la necesidad de mantener todo transparente 
            para una operación eficiente y sin sorpresas.
          </p>
          <p>
            Por eso creamos <strong class="brand">ControlAS</strong>: una aplicación web práctica, segura y 
            súper simple de usar (tan intuitiva que hasta un niño de 5 años podría manejarla). Está diseñada 
            específicamente para dueños que buscan profesionalizar su negocio y tener control total en tiempo real.
          </p>
        </div>

        <h3 class="features-title">Con ControlAS puedes:</h3>
        
        <div class="features-grid">
          <div v-for="(feature, index) in features" :key="index" class="feature-card" :style="{ animationDelay: `${index * 0.1}s` }">
            <div class="feature-icon">{{ feature.icon }}</div>
            <p>{{ feature.text }}</p>
          </div>
        </div>

        <div class="closing-text">
          <p>
            <strong class="brand">ControlAS</strong> es la forma del futuro para organizarte mejor: 
            olvídate de papelitos, exceles complicados o cuentas a mano. Todo queda registrado, seguro 
            y al alcance de tu celular o computador, con solo unos clics.
          </p>
          <p>
            El objetivo es entregarte una solución que te ahorre tiempo, minimice errores y te dé la 
            tranquilidad de tener las cuentas claras todos los días. En los negocios nocturnos, un control 
            estricto y confiable es lo que marca la diferencia entre una operación rentable y una llena de imprevistos.
          </p>
          <p class="cta-text">
            Si buscas llevar tu negocio a un nivel más profesional y seguro, 
            <strong class="brand">ControlAS</strong> es la herramienta que necesitas.
          </p>
          <button class="cta-button" @click="isMobile ? toggleContactModal() : toggleContactPanel()">
            ¡Contáctanos y te mostramos cómo funciona!
          </button>
        </div>
      </div>
    </section>

    <!-- Sección: Contáctanos -->
    <section class="section contact-section" :class="{ 'animate-in': section2Visible }" ref="section2">
      <div class="content-wrapper">
        <h2 class="section-title">
          <span class="title-line"></span>
          Contáctanos
          <span class="title-line"></span>
        </h2>
        
        <p class="contact-intro">
          ¿Quieres más información, una demostración o aclarar alguna duda sobre ControlAS? 
          Estamos aquí para ayudarte.
        </p>

        <div class="contact-methods">
          <a href="https://wa.me/573213686373" target="_blank" class="contact-card whatsapp-card">
            <div class="card-icon">📱</div>
            <h3>WhatsApp</h3>
            <p class="contact-detail">+57 321 368 6373</p>
            <span class="contact-action">Haz clic para chatear directo →</span>
          </a>

          <a href="mailto:controlas302025@gmail.com" class="contact-card email-card">
            <div class="card-icon">📧</div>
            <h3>Email</h3>
            <p class="contact-detail">controlas302025@gmail.com</p>
            <span class="contact-action">Haz clic para enviar correo →</span>
          </a>
        </div>

        <p class="contact-footer">
          ¡Estamos atentos para hablar de tu negocio y mostrarte cómo ControlAS puede facilitarte la vida!
        </p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ControlASLanding',
  data() {
    return {
      showContactModal: false,
      showContactPanel: false,
      section1Visible: false,
      section2Visible: false,
      isMobile: false,
      features: [
        {
          icon: '🏢',
          text: 'Gestionar múltiples establecimientos desde un solo lugar (bares y burdeles)'
        },
        {
          icon: '📦',
          text: 'Llevar el inventario completo con registro automático de todos los movimientos'
        },
        {
          icon: '💰',
          text: 'Generar la factura diaria de manera sencilla: el sistema calcula automáticamente lo vendido, lo perdido y el resultado neto del día'
        },
        {
          icon: '👁️',
          text: 'Supervisar a los administradores con trazabilidad completa de sus acciones'
        },
        {
          icon: '⚕️',
          text: 'Recibir alertas automáticas cuando los exámenes médicos del personal estén por vencer, evitando multas y sanciones'
        },
        {
          icon: '🚀',
          text: 'Entre otras cosas y futuras actualizaciones'
        }
      ]
    };
  },
  mounted() {
    this.setupIntersectionObserver();
    this.checkMobile();
    window.addEventListener('resize', this.checkMobile);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
  },
  methods: {
    toggleContactModal() {
      this.showContactModal = !this.showContactModal;
    },
    toggleContactPanel() {
      this.showContactPanel = !this.showContactPanel;
    },
    checkMobile() {
      this.isMobile = window.innerWidth < 1024;
    },
    setupIntersectionObserver() {
      const options = {
        threshold: 0.2,
        rootMargin: '0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.target === this.$refs.section1) {
            this.section1Visible = entry.isIntersecting;
          }
          if (entry.target === this.$refs.section2) {
            this.section2Visible = entry.isIntersecting;
          }
        });
      }, options);

      if (this.$refs.section1) observer.observe(this.$refs.section1);
      if (this.$refs.section2) observer.observe(this.$refs.section2);
    }
  }
};
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.controlas-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #000000 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
}

/* Panel lateral de contacto (Desktop) */
.contact-sidebar {
  position: fixed;
  right: -350px;
  top: 0;
  width: 350px;
  height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-left: 3px solid rgba(255, 20, 147, 0.5);
  box-shadow: -10px 0 40px rgba(0, 0, 0, 0.5);
  transition: right 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 900;
  overflow-y: auto;
}

.contact-sidebar.open {
  right: 0;
}

.sidebar-content {
  padding: 40px 30px;
}

.sidebar-content h3 {
  color: #ff69b4;
  font-size: 28px;
  margin-bottom: 10px;
  text-align: center;
}

.sidebar-subtitle {
  text-align: center;
  color: #ccc;
  margin-bottom: 40px;
  font-size: 16px;
}

.sidebar-footer {
  text-align: center;
  color: #ff69b4;
  margin-top: 30px;
  font-size: 16px;
  font-weight: 600;
}

/* Tab de contacto (Desktop) */
.contact-tab {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  padding: 20px 12px;
  border-radius: 15px 0 0 15px;
  cursor: pointer;
  z-index: 1000;
  box-shadow: -5px 0 20px rgba(255, 20, 147, 0.5);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

.contact-tab:hover {
  padding-right: 18px;
  box-shadow: -8px 0 30px rgba(255, 20, 147, 0.7);
}

.contact-tab span {
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 2px;
}

.contact-tab svg {
  transform: rotate(90deg);
}

/* Botón flotante móvil */
.floating-contact-mobile {
  position: fixed;
  bottom: 25px;
  right: 25px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  border-radius: 50%;
  display: none;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 30px rgba(255, 20, 147, 0.6);
  cursor: pointer;
  z-index: 1000;
  animation: float 3s ease-in-out infinite;
  transition: transform 0.3s ease;
}

.floating-contact-mobile:active {
  transform: scale(0.95);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Mostrar botón flotante solo en mobile */
@media (max-width: 1023px) {
  .contact-tab {
    display: none;
  }
  
  .contact-sidebar {
    display: none;
  }
  
  .floating-contact-mobile {
    display: flex;
  }
}

/* Modal de contacto (Mobile) */
.contact-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.contact-modal {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 25px;
  padding: 35px 25px;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(255, 20, 147, 0.4);
  max-height: 90vh;
  overflow-y: auto;
}

.contact-modal h3 {
  color: #ff69b4;
  font-size: 26px;
  margin-bottom: 10px;
  text-align: center;
}

.modal-subtitle {
  text-align: center;
  color: #ccc;
  margin-bottom: 30px;
  font-size: 15px;
}

.contact-option {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 18px;
  border-radius: 15px;
  margin-bottom: 15px;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.contact-option.whatsapp {
  background: linear-gradient(135deg, #25D366, #128C7E);
  color: white;
}

.contact-option.email {
  background: linear-gradient(135deg, #4285F4, #1967D2);
  color: white;
}

.contact-option:hover {
  transform: translateX(5px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
}

.contact-option:active {
  transform: translateX(2px);
}

.contact-icon-wrapper {
  background: rgba(255, 255, 255, 0.2);
  padding: 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
  min-width: 0;
}

.contact-info strong {
  font-size: 17px;
}

.contact-info span {
  font-size: 14px;
  opacity: 0.95;
  word-break: break-word;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

/* Secciones */
.section {
  padding: 80px 20px;
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.8s ease;
}

.section.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 42px;
  text-align: center;
  margin-bottom: 40px;
  color: #ff69b4;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px #ff69b4, 0 0 20px #ff69b4, 0 0 30px #ff1493;
  }
  to {
    text-shadow: 0 0 20px #ff69b4, 0 0 30px #ff69b4, 0 0 40px #ff1493;
  }
}

.title-line {
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #ff69b4, transparent);
}

/* Quiénes Somos */
.who-we-are {
  background: linear-gradient(135deg, #0a0a1e 0%, #1a1a2e 100%);
}

.intro-text p {
  font-size: 17px;
  line-height: 1.8;
  margin-bottom: 20px;
  color: #e0e0e0;
}

.brand {
  color: #ff69b4;
  font-weight: 700;
}

.features-title {
  font-size: 28px;
  color: #4da6ff;
  margin: 40px 0 30px;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
  margin: 35px 0;
}

.feature-card {
  background: linear-gradient(135deg, #16213e, #0f3460);
  border: 2px solid rgba(77, 166, 255, 0.3);
  border-radius: 20px;
  padding: 25px;
  transition: all 0.4s ease;
  animation: slideIn 0.6s ease forwards;
  opacity: 0;
}

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(77, 166, 255, 0.4);
  border-color: #4da6ff;
}

.feature-icon {
  font-size: 42px;
  margin-bottom: 15px;
}

.feature-card p {
  font-size: 15px;
  line-height: 1.6;
  color: #d0d0d0;
}

.closing-text {
  margin-top: 40px;
}

.closing-text p {
  font-size: 17px;
  line-height: 1.8;
  margin-bottom: 20px;
  color: #e0e0e0;
}

.cta-text {
  font-size: 20px !important;
  color: #ff69b4 !important;
  font-weight: 600;
  margin-top: 35px !important;
  text-align: center;
}

.cta-button {
  display: block;
  margin: 30px auto 0;
  padding: 16px 35px;
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(255, 20, 147, 0.4);
}

.cta-button:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 35px rgba(255, 20, 147, 0.6);
}

.cta-button:active {
  transform: scale(0.98);
}

/* Contacto */
.contact-section {
  background: linear-gradient(135deg, #1a1a2e 0%, #0a0a1e 100%);
}

.contact-intro {
  font-size: 19px;
  text-align: center;
  margin-bottom: 50px;
  color: #e0e0e0;
  line-height: 1.8;
}

.contact-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin: 60px 0;
}

.contact-card {
  background: linear-gradient(135deg, #16213e, #0f3460);
  border-radius: 25px;
  padding: 40px;
  text-align: center;
  text-decoration: none;
  color: white;
  border: 3px solid transparent;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.contact-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.contact-card:hover::before {
  left: 100%;
}

.whatsapp-card {
  border-color: #25D366;
}

.whatsapp-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 50px rgba(37, 211, 102, 0.4);
}

.email-card {
  border-color: #4285F4;
}

.email-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 50px rgba(66, 133, 244, 0.4);
}

.card-icon {
  font-size: 64px;
  margin-bottom: 20px;
  animation: bounce 2s ease infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

.contact-card h3 {
  font-size: 28px;
  margin-bottom: 15px;
  color: #ff69b4;
}

.contact-detail {
  font-size: 18px;
  margin-bottom: 20px;
  color: #d0d0d0;
  font-weight: 600;
}

.contact-action {
  display: inline-block;
  margin-top: 15px;
  color: #4da6ff;
  font-weight: 600;
  font-size: 16px;
}

.contact-footer {
  text-align: center;
  font-size: 20px;
  color: #ff69b4;
  font-weight: 600;
  margin-top: 40px;
}

/* Responsive - Tablet */
@media (max-width: 768px) {
  .section {
    padding: 60px 15px;
  }

  .section-title {
    font-size: 32px;
    gap: 15px;
  }

  .title-line {
    width: 50px;
  }

  .intro-text p,
  .closing-text p {
    font-size: 16px;
  }

  .features-title {
    font-size: 24px;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .feature-card {
    padding: 20px;
  }

  .feature-icon {
    font-size: 36px;
  }

  .cta-text {
    font-size: 18px !important;
  }

  .cta-button {
    padding: 14px 30px;
    font-size: 16px;
  }

  .contact-intro {
    font-size: 17px;
  }

  .contact-methods {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .contact-card {
    padding: 30px;
  }

  .card-icon {
    font-size: 52px;
  }

  .contact-card h3 {
    font-size: 24px;
  }

  .contact-detail {
    font-size: 16px;
  }

  .contact-footer {
    font-size: 18px;
  }
}

/* Responsive - Mobile */
@media (max-width: 480px) {
  .section {
    padding: 50px 12px;
  }

  .section-title {
    font-size: 28px;
    gap: 10px;
  }

  .title-line {
    width: 40px;
  }

  .intro-text p,
  .closing-text p {
    font-size: 15px;
  }

  .features-title {
    font-size: 22px;
  }

  .feature-card {
    padding: 18px;
  }

  .feature-card p {
    font-size: 14px;
  }

  .feature-icon {
    font-size: 32px;
  }

  .cta-text {
    font-size: 17px !important;
  }

  .cta-button {
    padding: 12px 25px;
    font-size: 15px;
  }

  .contact-intro {
    font-size: 16px;
  }

  .contact-card {
    padding: 25px 20px;
  }

  .card-icon {
    font-size: 48px;
  }

  .contact-card h3 {
    font-size: 22px;
  }

  .contact-detail {
    font-size: 15px;
    word-break: break-all;
  }

  .contact-action {
    font-size: 14px;
  }

  .contact-footer {
    font-size: 16px;
  }

  .floating-contact-mobile {
    bottom: 20px;
    right: 20px;
    width: 55px;
    height: 55px;
  }

  .contact-modal {
    padding: 30px 20px;
    border-radius: 20px;
  }

  .contact-modal h3 {
    font-size: 24px;
  }

  .modal-subtitle {
    font-size: 14px;
  }

  .contact-option {
    padding: 15px;
    gap: 12px;
  }

  .contact-icon-wrapper {
    padding: 10px;
  }

  .contact-info strong {
    font-size: 16px;
  }

  .contact-info span {
    font-size: 13px;
  }

  .sidebar-footer {
    font-size: 15px;
  }
}

/* Responsive - Large screens */
@media (min-width: 1400px) {
  .content-wrapper {
    max-width: 1400px;
  }

  .section-title {
    font-size: 52px;
  }

  .intro-text p,
  .closing-text p {
    font-size: 19px;
  }

  .features-title {
    font-size: 34px;
  }

  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .feature-card p {
    font-size: 16px;
  }

  .cta-text {
    font-size: 24px !important;
  }

  .cta-button {
    padding: 18px 45px;
    font-size: 20px;
  }

  .contact-intro {
    font-size: 21px;
  }

  .contact-methods {
    grid-template-columns: repeat(2, 1fr);
    gap: 50px;
  }
}
</style>